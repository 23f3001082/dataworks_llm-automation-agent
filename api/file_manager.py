import os

def read_file(path: str) -> str:
    if not path.startswith("/data/"):
        raise PermissionError("Access outside /data/ is restricted.")
    
    if not os.path.exists(path):
        raise FileNotFoundError()

    with open(path, 'r') as f:
        return f.read()
    


def list_files(directory_path: str, extension: str = None):
    """
    Lists all files in a directory.
    If an extension is provided, filters files by that extension.
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory {directory_path} not found.")

    files = os.listdir(directory_path)
    
    if extension:
        files = [file for file in files if file.endswith(extension)]
    
    return files