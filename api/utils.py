import subprocess
import json
import os
from datetime import datetime

def run_datagen(user_email: str):
    subprocess.run(["python3", "datagen.py", user_email])

def format_markdown(file_path: str):
    subprocess.run(["prettier", "--write", file_path])

def count_wednesdays(input_path: str, output_path: str):
    with open(input_path, "r") as file:
        dates = file.readlines()
    wednesdays = [date.strip() for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2]
    with open(output_path, "w") as file:
        file.write(str(len(wednesdays)))

def execute_shell(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing command: {str(e)}"

# ✅ New Function: Read JSON File
def read_json(file_path: str):
    """Reads a JSON file and returns its contents as a dictionary."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ✅ New Function: Write Content to a File
def write_to_file(file_path: str, content: str):
    """Writes content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# ✅ New Function: List Files in a Directory
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