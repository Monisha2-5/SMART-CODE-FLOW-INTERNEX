import sqlite3
import datetime
import json
import os

PRIMARY_DB = "smartcodeflow.db"
LEGACY_DB = "smart_code_flow.db"

def init_db():
    """Initialize the SQLite database and create necessary tables in both databases."""
    # Initialize primary database with rich schema
    conn = sqlite3.connect(PRIMARY_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            language TEXT,
            coding_standard TEXT,
            quality_score INTEGER,
            total_findings INTEGER,
            critical_count INTEGER,
            high_count INTEGER,
            medium_count INTEGER,
            low_count INTEGER,
            review_date TEXT,
            submitted_code TEXT,
            findings_json TEXT
        )
    """)
    conn.commit()
    conn.close()

    # Legacy database compatibility
    conn_leg = sqlite3.connect(LEGACY_DB)
    cursor_leg = conn_leg.cursor()
    cursor_leg.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            quality_score INTEGER,
            critical_count INTEGER,
            high_count INTEGER,
            medium_count INTEGER,
            low_count INTEGER,
            created_at TIMESTAMP
        )
    """)
    conn_leg.commit()
    conn_leg.close()

def save_review_record(file_name, score, critical, high, medium, low):
    """Save a completed review session to the legacy database for backwards compatibility."""
    now = datetime.datetime.now()
    conn = sqlite3.connect(LEGACY_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (file_name, quality_score, critical_count, high_count, medium_count, low_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (file_name, score, critical, high, medium, low, now))
    conn.commit()
    conn.close()

    # Also persist into primary database
    save_full_review(
        file_name=file_name,
        language="Python",
        coding_standard="PEP 8",
        quality_score=score,
        total_findings=(critical + high + medium + low),
        critical_count=critical,
        high_count=high,
        medium_count=medium,
        low_count=low,
        submitted_code="",
        findings_json="[]"
    )

def save_full_review(file_name, language, coding_standard, quality_score, total_findings,
                     critical_count, high_count, medium_count, low_count, submitted_code, findings_json):
    """Save a comprehensive review session with code and JSON findings."""
    init_db()
    now_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    conn = sqlite3.connect(PRIMARY_DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO review_history (
            file_name, language, coding_standard, quality_score, total_findings,
            critical_count, high_count, medium_count, low_count, review_date,
            submitted_code, findings_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        file_name, language, coding_standard, quality_score, total_findings,
        critical_count, high_count, medium_count, low_count, now_str,
        submitted_code, findings_json if isinstance(findings_json, str) else json.dumps(findings_json)
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Also sync legacy DB
    try:
        conn_leg = sqlite3.connect(LEGACY_DB)
        cursor_leg = conn_leg.cursor()
        cursor_leg.execute("""
            INSERT INTO reviews (file_name, quality_score, critical_count, high_count, medium_count, low_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (file_name, quality_score, critical_count, high_count, medium_count, low_count, datetime.datetime.now()))
        conn_leg.commit()
        conn_leg.close()
    except Exception:
        pass

    return new_id

def get_review_history():
    """Retrieve all past reviews from the database (legacy tuple format)."""
    conn = sqlite3.connect(LEGACY_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_name, quality_score, critical_count, high_count, medium_count, low_count, created_at FROM reviews ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_detailed_review_history():
    """Retrieve rich review history objects with full fields for the UI."""
    init_db()
    conn = sqlite3.connect(PRIMARY_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, file_name, language, coding_standard, quality_score, total_findings,
               critical_count, high_count, medium_count, low_count, review_date,
               submitted_code, findings_json
        FROM review_history
        ORDER BY id DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_review_by_id(review_id):
    """Retrieve a single review record by ID."""
    init_db()
    conn = sqlite3.connect(PRIMARY_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM review_history WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_dashboard_analytics():
    """Return actual aggregated metrics and dataset from the databases for the Dashboard."""
    reviews = get_detailed_review_history()
    
    total_reviews = len(reviews)
    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "avg_score": 0,
            "total_issues": 0,
            "projects_count": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "timeline": [],
            "weekly_counts": [0]*7
        }
    
    avg_score = round(sum(r["quality_score"] or 0 for r in reviews) / total_reviews)
    critical = sum(r["critical_count"] or 0 for r in reviews)
    high = sum(r["high_count"] or 0 for r in reviews)
    medium = sum(r["medium_count"] or 0 for r in reviews)
    low = sum(r["low_count"] or 0 for r in reviews)
    total_issues = critical + high + medium + low
    unique_projects = len(set(r["file_name"] for r in reviews if r.get("file_name")))
    
    # Timeline data for Line Chart (chronological)
    chronological = list(reversed(reviews))
    timeline = []
    for idx, r in enumerate(chronological):
        timeline.append({
            "Review": f"Rev #{r['id']}",
            "Date": r["review_date"][:10] if r.get("review_date") else f"Day {idx+1}",
            "Score": r["quality_score"] or 80,
            "Issues": r["total_findings"] or 0
        })
        
    return {
        "total_reviews": total_reviews,
        "avg_score": avg_score,
        "total_issues": total_issues,
        "projects_count": max(unique_projects, 1),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "timeline": timeline,
        "reviews": reviews
    }
