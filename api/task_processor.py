import os
import subprocess
import json
from datetime import datetime
from api.llm_handler import parse_task
from api.utils import execute_shell, read_json, write_to_file, sort_json, extract_email
from api.file_manager import list_files


# ✅ Define base directory for resolving file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def execute_task(task_description: str):
   def execute_task(task_description: str):
    """Parses the task and executes the appropriate function."""
    parsed_task = parse_task(task_description).lower().strip()

    # ✅ Debugging: Print parsed task
    print(f"DEBUG: Parsed Task - {parsed_task}")

    # if "install uv and run datagen.py" in parsed_task:
    #     email = "23f3001082@ds.study.iitm.ac.in"  # Ensure this is your IITM email
    #     return execute_shell(f"pip install uv && python datagen.py {email}")
    if "install uv" in parsed_task and "datagen.py" in parsed_task:
        return install_uv_and_run_datagen()  

    elif any(keyword in parsed_task for keyword in ["format markdown", "prettier", "format md", "format markdown file"]):
        file_path = "/data/format.md"

        if not os.path.exists(file_path):
            print(f"ERROR: File {file_path} not found!")
            return f"Error: File {file_path} not found!"

        # ✅ Run Prettier inside the container
        command = f"npx prettier --write {file_path}"
        print(f"DEBUG: Running command - {command}")
        
        result = execute_shell(command)
        
        # ✅ Debugging: Print the output from Prettier
        print(f"DEBUG: Prettier Output - {result}")
        
        return f"Formatted {file_path}"
    elif "count wednesdays" in parsed_task:
        return count_weekdays(os.path.join(BASE_DIR, "dates.txt"), "Wednesday")

    elif "sort contacts" in parsed_task or "sort contacts in" in parsed_task:
        input_path = os.path.join(BASE_DIR, "contacts.json")
        output_path = os.path.join(BASE_DIR, "contacts-sorted.json")

        # ✅ Debugging: Print absolute paths being used
        print(f"DEBUG: Looking for input file at: {input_path}")
        print(f"DEBUG: Output file will be saved at: {output_path}")

        result = sort_json(input_path, output_path)  # ✅ Use absolute paths

        # ✅ Debugging: Print the function output
        print(f"DEBUG: Result from sort_json - {result}")

        return result
        
    elif "extract sender email" in parsed_task:
        return extract_email("/data/email.txt") 
    else:
        print(f"ERROR: Task '{task_description}' not recognized.")
        raise ValueError("Task not recognized")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def count_weekdays(file_path, weekday):
    """Counts the occurrences of a specific weekday from a list of dates."""

    # Ensure file path is resolved correctly
    if not os.path.isabs(file_path):
        file_path = os.path.join(BASE_DIR, os.path.basename(file_path))

    print(f"DEBUG: Resolving file path - {file_path}")

    if not os.path.exists(file_path):
        print(f"ERROR: File not found - {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        dates = f.readlines()

    count = sum(
        1 for date in dates
        if date.strip() and
        valid_date_format(date.strip()) and
        datetime.strptime(format_date(date.strip()), "%Y-%m-%d").weekday() == 2
    )

    result_file = f"{file_path[:-4]}-wednesdays.txt"
    write_to_file(result_file, str(count))

    print(f"DEBUG: Counted {count} {weekday}s. Result saved to {result_file}")

    return f"Counted {count} {weekday}s"

def valid_date_format(date_str):
    """Helper function to check if a date is valid in known formats."""
    valid_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    for fmt in valid_formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    return False

def format_date(date_str):
    """Helper function to convert different date formats into standard YYYY-MM-DD format."""
    valid_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    for fmt in valid_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")


def install_uv_and_run_datagen():
    """Installs uv if not present and runs datagen.py"""
    email = "23f3001082@ds.study.iitm.ac.in"  # Replace with dynamic user input if needed

    # Check if `uv` is installed
    uv_check = subprocess.run(["which", "uv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if not uv_check.stdout.strip():
        print("DEBUG: `uv` not found. Installing...")
        install_output = execute_shell("pip install uv")
        print(f"DEBUG: uv installation output: {install_output}")

    # Run datagen.py
    command = f"python datagen.py {email}"
    print(f"DEBUG: Running {command}...")
    datagen_output = execute_shell(command)

    return f"✅ Completed Task A1: {datagen_output}"