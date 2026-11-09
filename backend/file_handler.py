import os
import zipfile
import tempfile

def read_python_file(file_path):
    """Read the text content of a single Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")

def extract_project_zip(zip_file_path, extract_to_dir=None):
    """Extract an uploaded ZIP archive containing a Python project."""
    if not extract_to_dir:
        extract_to_dir = tempfile.mkdtemp()
        
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_dir)
        return {"success": True, "extracted_path": extract_to_dir}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_python_files(directory_path):
    """Recursively find all .py files in a given project directory."""
    py_files = []
    for root, dirs, files in os.walk(directory_path):
        # Ignore virtual environments or hidden folders like .git
        if any(ignored in root for ignored in ['.git', '__pycache__', 'venv', 'env']):
            continue
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files