import subprocess
import json
import os
from datetime import datetime

def execute_shell(command: str):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing command: {str(e)}"

def read_json(file_path: str):
    """Reads a JSON file and returns its contents as a dictionary."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_to_file(file_path: str, content: str):
    """Writes content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def list_files(directory_path: str, extension: str = None):
    """Lists all files in a directory with an optional extension filter."""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory {directory_path} not found.")
    files = os.listdir(directory_path)
    if extension:
        files = [file for file in files if file.endswith(extension)]
    return files

def sort_json(input_path: str, output_path: str):
    """Sorts a JSON file alphabetically by last_name and saves it to output file."""
    print(f"DEBUG: Checking input file - {input_path}")
    if not os.path.exists(input_path):
        return f"Error: File {input_path} not found"
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return f"Error: Expected a JSON array but found {type(data)}"
        sorted_data = sorted(data, key=lambda x: x.get("last_name", "").lower())
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sorted_data, f, indent=4)
        print(f"DEBUG: Sorted contacts saved to {output_path}")
        return f"Sorted contacts successfully saved to {output_path}"
    except Exception as e:
        return f"Error sorting JSON: {str(e)}"

def extract_email(file_path: str):
    """Extracts sender's email address from a text file."""
    real_path = os.path.abspath(os.path.join(BASE_DIR, os.path.basename(file_path)))
    print(f"DEBUG: Looking for file at {real_path}")
    if not os.path.exists(real_path):
        return f"Error: File {real_path} not found"
    with open(real_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"From:\s*\"?.*?\"?\s*<([^>]+)>", content)
    if match:
        sender_email = match.group(1)
        return f"Extracted sender email: {sender_email}"
    else:
        return "No sender email found."