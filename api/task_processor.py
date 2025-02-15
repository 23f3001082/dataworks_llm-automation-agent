import os
import subprocess
import json
from datetime import datetime
from api.llm_handler import parse_task
from api.utils import execute_shell, read_json, write_to_file, sort_json, extract_email
from api.file_manager import list_files

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def execute_task(task_description: str):
    """Parses the task and executes the appropriate function."""
    parsed_task = parse_task(task_description).lower().strip()
    print(f"DEBUG: Parsed Task - {parsed_task}")

    if "install uv" in parsed_task and "datagen.py" in parsed_task:
        return install_uv_and_run_datagen()
    elif any(keyword in parsed_task for keyword in ["format markdown", "prettier", "format md", "format markdown file"]):
        return format_markdown("/data/format.md")
    elif "count wednesdays" in parsed_task:
        return count_weekdays(os.path.join(BASE_DIR, "dates.txt"), "Wednesday")
    elif "sort contacts" in parsed_task or "sort contacts in" in parsed_task:
        return sort_contacts(os.path.join(BASE_DIR, "contacts.json"), os.path.join(BASE_DIR, "contacts-sorted.json"))
    elif "extract sender email" in parsed_task:
        return extract_email("/data/email.txt")
    elif "markdown index" in parsed_task or "create index" in parsed_task:
        return create_markdown_index("./data/docs", "./data/docs/index.json")
    else:
        print(f"ERROR: Task '{task_description}' not recognized.")
        raise ValueError("Task not recognized")

def install_uv_and_run_datagen():
    """Installs uv if not present and runs datagen.py"""
    email = "23f3001082@ds.study.iitm.ac.in"
    uv_check = subprocess.run(["which", "uv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if not uv_check.stdout.strip():
        print("DEBUG: `uv` not found. Installing...")
        install_output = execute_shell("pip install uv")
        print(f"DEBUG: uv installation output: {install_output}")
    command = f"python datagen.py {email}"
    print(f"DEBUG: Running {command}...")
    datagen_output = execute_shell(command)
    return f"✅ Completed Task A1: {datagen_output}"

def format_markdown(file_path: str):
    """Formats a markdown file using Prettier."""
    if not os.path.exists(file_path):
        return f"Error: File {file_path} not found!"
    command = f"npx prettier --write {file_path}"
    print(f"DEBUG: Running command - {command}")
    result = execute_shell(command)
    print(f"DEBUG: Prettier Output - {result}")
    return f"Formatted {file_path}"

def count_weekdays(file_path: str, weekday: str):
    """Counts the occurrences of a specific weekday from a list of dates."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as f:
        dates = f.readlines()
    count = sum(1 for date in dates if valid_date_format(date.strip()) and datetime.strptime(format_date(date.strip()), "%Y-%m-%d").weekday() == 2)
    result_file = f"{file_path[:-4]}-wednesdays.txt"
    write_to_file(result_file, str(count))
    return f"Counted {count} {weekday}s"

def sort_contacts(input_path: str, output_path: str):
    """Sorts contacts by last_name and first_name."""
    if not os.path.exists(input_path):
        return f"Error: File {input_path} not found"
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sorted_data = sorted(data, key=lambda x: (x.get("last_name", "").lower(), x.get("first_name", "").lower()))
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sorted_data, f, indent=4)
        return f"Sorted contacts successfully saved to {output_path}"
    except Exception as e:
        return f"Error sorting JSON: {str(e)}"

def valid_date_format(date_str: str):
    """Helper function to check if a date is valid in known formats."""
    valid_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    for fmt in valid_formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    return False

def format_date(date_str: str):
    """Helper function to convert different date formats into standard YYYY-MM-DD format."""
    valid_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    for fmt in valid_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")



def get_recent_logs(directory_path: str, output_path: str):
    """Writes the first line of the 10 most recent .log files to a file."""
    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} not found"
    log_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".log")]
    log_files.sort(key=os.path.getmtime, reverse=True)
    recent_logs = log_files[:10]
    first_lines = []
    for log_file in recent_logs:
        with open(log_file, "r", encoding="utf-8") as f:
            first_lines.append(f.readline().strip())
    write_to_file(output_path, "\n".join(first_lines))
    return f"First lines of 10 most recent logs written to {output_path}"


import os
import json

def create_markdown_index(directory_path: str, output_path: str):
    """
    Creates an index of Markdown files with their first H1 title.
    Args:
        directory_path (str): Path to the directory containing Markdown files.
        output_path (str): Path to save the index JSON file.
    Returns:
        str: Success or error message.
    """
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} not found."

    # Find all .md files in the directory (including subdirectories)
    md_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):
                # Store the relative path to the file
                relative_path = os.path.relpath(os.path.join(root, file), directory_path)
                md_files.append(relative_path)

    # Create the index
    index = {}
    for md_file in md_files:
        full_path = os.path.join(directory_path, md_file)
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    # Extract the title (remove the "# " prefix and strip whitespace)
                    title = line.strip("# ").strip()
                    index[md_file] = title
                    break  # Stop after the first H1

    # Write the index to the output file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)
        return f"Markdown index created at {output_path}"
    except Exception as e:
        return f"Error writing index file: {str(e)}"



def create_markdown_index(directory_path: str, output_path: str):
    """
    Creates an index of Markdown files with their first H1 title.
    Args:
        directory_path (str): Path to the directory containing Markdown files.
        output_path (str): Path to save the index JSON file.
    Returns:
        str: Success or error message.
    """
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} not found."

    # Find all .md files in the directory (including subdirectories)
    md_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):
                # Store the relative path to the file
                relative_path = os.path.relpath(os.path.join(root, file), directory_path)
                md_files.append(relative_path)

    # Create the index
    index = {}
    for md_file in md_files:
        full_path = os.path.join(directory_path, md_file)
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    # Extract the title (remove the "# " prefix and strip whitespace)
                    title = line.strip("# ").strip()
                    index[md_file] = title
                    break  # Stop after the first H1

    # Write the index to the output file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)
        return f"Markdown index created at {output_path}"
    except Exception as e:
        return f"Error writing index file: {str(e)}"