import json
import datetime

def generate_markdown_report(project_name, score, findings, stats):
    """Generate a structured Markdown audit report."""
    report = f"""# SmartCodeFlow Audit Report
- **Project / File**: {project_name}
- **Generated Date**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Overall Quality Score**: {score} / 100

## Executive Summary
- **Critical Issues**: {stats.get('critical', 0)}
- **High Severity Issues**: {stats.get('high', 0)}
- **Medium Severity Issues**: {stats.get('medium', 0)}
- **Low Severity Issues**: {stats.get('low', 0)}

## Detailed Review Findings
"""
    for idx, finding in enumerate(findings, 1):
        report += f"""
### {idx}. {finding.get('title', 'Security / Quality Finding')}
- **Severity**: {finding.get('severity', 'Unknown')}
- **Category**: {finding.get('category', 'General')}
- **Line Reference**: {finding.get('line', 'N/A')}
- **Problem Description**: {finding.get('problem', '')}
- **Suggested Fix**:
  ```python
  {finding.get('suggested_fix', '# Apply appropriate refactoring')}
  ```
"""
    return report
