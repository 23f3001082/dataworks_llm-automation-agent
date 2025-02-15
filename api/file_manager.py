# import os


# # Define the allowed base directory
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

# def read_file(path: str) -> str:
#     """Reads a file and returns its content as a string."""

#     # Ensure the requested file is inside /data/
#     full_path = os.path.abspath(os.path.join(BASE_DIR, os.path.basename(path)))

#     if not full_path.startswith(BASE_DIR):
#         raise PermissionError("Access outside /data/ is restricted.")

#     # Ensure file exists
#     if not os.path.isfile(full_path):
#         raise FileNotFoundError(f"File not found: {full_path}")

#     # Read and return file content
#     with open(full_path, "r", encoding="utf-8") as f:
#         return f.read()


import os

# Define the allowed base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def read_file(path: str) -> str:
    """Reads a file and returns its content as a string."""
    
    # ✅ Debugging: Print initial requested path
    print(f"DEBUG: Requested file path - {path}")

    # Normalize and construct the absolute path
    full_path = os.path.abspath(os.path.join(BASE_DIR, os.path.basename(path)))

    # ✅ Debugging: Print constructed full path
    print(f"DEBUG: Resolved full path - {full_path}")

    # Ensure the requested file is inside /data/
    if not full_path.startswith(BASE_DIR):
        print(f"ERROR: Attempt to access outside /data/ - {full_path}")
        raise PermissionError(f"Access outside /data/ is restricted: {full_path}")

    # Ensure file exists
    if not os.path.isfile(full_path):
        print(f"ERROR: File not found - {full_path}")
        raise FileNotFoundError(f"File not found: {full_path}")

    # ✅ Debugging: File exists, proceeding to read
    print(f"DEBUG: Reading file - {full_path}")

    # Read and return file content
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # ✅ Debugging: Print file content length
    print(f"DEBUG: File read successfully - {len(content)} characters")

    return content

def list_files(directory_path: str, extension: str = None):
    """Lists all files in a directory with an optional extension filter."""
    
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory {directory_path} not found.")

    files = os.listdir(directory_path)
    
    # Filter files by extension if provided
    if extension:
        files = [file for file in files if file.endswith(extension)]
    
    return files