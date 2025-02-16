import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def read_file(path: str) -> str:
    
    """Reads a file and returns its content as a string."""
    print(f"DEBUG: Requested file path - {path}")
    full_path = os.path.abspath(os.path.join(BASE_DIR, os.path.basename(path)))
    print(f"DEBUG: Resolved full path - {full_path}")

    if not full_path.startswith(BASE_DIR):
        print(f"ERROR: Attempt to access outside /data/ - {full_path}")
        raise PermissionError(f"Access outside /data/ is restricted: {full_path}")

    if not os.path.isfile(full_path):
        print(f"ERROR: File not found - {full_path}")
        raise FileNotFoundError(f"File not found: {full_path}")

    print(f"DEBUG: Reading file - {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"DEBUG: File read successfully - {len(content)} characters")
    return content


def list_files(directory_path: str, extension: str = None):
    """Lists all files in a directory with an optional extension filter."""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory {directory_path} not found.")
    files = os.listdir(directory_path)
    if extension:
        files = [file for file in files if file.endswith(extension)]
    return files