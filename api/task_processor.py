import os
import subprocess
import json
import re
from datetime import datetime
from PIL import Image
import pytesseract

from api.utils import execute_shell, write_to_file, sort_json, extract_sender_email, read_json
from api.file_manager import list_files

# ✅ Define base directory for resolving file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def execute_task(task_description: str):
    """Parses the task and executes the appropriate function."""
    
    parsed_task = task_description.lower().strip()
    print(f"DEBUG: BASE_DIR - {BASE_DIR}")
    print(f"DEBUG: Parsed Task - {parsed_task}")

    # ✅ Task A1: Install UV and Run Datagen
    if "install uv" in parsed_task or "datagen.py" in parsed_task:
        return install_uv_and_run_datagen()
    
    # ✅ Task A2: Format Markdown File
    elif any(keyword in parsed_task for keyword in ["format markdown", "prettier", "format md", "format markdown file"]):
        return format_markdown(os.path.join(BASE_DIR, "format.md"))

    # ✅ Task A3: Count Weekdays
    elif parsed_task.startswith("count ") and parsed_task.split()[1] in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        weekday = parsed_task.split()[1]  # Extract weekday dynamically
        return count_weekdays(os.path.join(BASE_DIR, "dates.txt"), weekday)
    
    # ✅ Task A4: Sort Contacts
    elif "sort contacts" in parsed_task:
        return sort_contacts(os.path.join(BASE_DIR, "contacts.json"), os.path.join(BASE_DIR, "contacts-sorted.json"))

    # ✅ Task A5: Extract Sender Email
    elif "extract sender email" in parsed_task:
        return extract_sender_email(os.path.join(BASE_DIR, "email.txt"), os.path.join(BASE_DIR, "email-sender.txt"))
    
    # ✅ Task A6: Extract Credit Card from Image
    elif "extract credit card" in parsed_task or "credit card number" in parsed_task:
        return extract_credit_card_number(os.path.join(BASE_DIR, "credit_card.png"), os.path.join(BASE_DIR, "credit_card.txt"))
    
    # ✅ Task A7: Create Markdown Index
    elif "markdown index" in parsed_task or "create index" in parsed_task:
        return create_markdown_index("./data/docs/", "./data/docs/index.json") 

    elif "get recent logs" in parsed_task:
        return get_recent_logs("./data/logs/", "./data/recent-logs.txt")

    # ❌ Unrecognized Task
    else:
        print(f"ERROR: Task '{task_description}' not recognized.")
        raise ValueError("Task not recognized")


# ✅ Task A1: Install UV and Run Datagen
def install_uv_and_run_datagen():
    """Installs uv if not present and runs datagen.py."""
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


# ✅ Task A2: Format Markdown File
def format_markdown(file_path: str):
    """Formats a markdown file using Prettier."""
    if not os.path.exists(file_path):
        return f"Error: File {file_path} not found!"
    
    command = f"npx prettier --write {file_path}"
    print(f"DEBUG: Running command - {command}")
    result = execute_shell(command)
    print(f"DEBUG: Prettier Output - {result}")
    return f"Formatted {file_path}"


# ✅ Task A3: Count Weekdays in Dates File
def count_weekdays(file_path: str, weekday: str):
    """Counts occurrences of a given weekday from a list of dates."""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        dates = f.readlines()

    count = 0
    for date in dates:
        date = date.strip()
        if date and valid_date_format(date):
            formatted_date = format_date(date)
            day_name = datetime.strptime(formatted_date, "%Y-%m-%d").strftime('%A')
            if day_name.lower() == weekday.lower():
                count += 1  # ✅ Properly counts the matching weekdays

    # ✅ Store result in `/data/dates-count.txt`
    result_file = os.path.join(BASE_DIR, "dates-count.txt")
    write_to_file(result_file, str(count))

    # ✅ Fixes extra "s" issue in response message
    return f"✅ Counted {count} {weekday}"


# ✅ Helper Functions for Date Handling
def valid_date_format(date_str):
    valid_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    for fmt in valid_formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    return False

def format_date(date_str):
    valid_formats = ["%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d %H:%M:%S"]
    for fmt in valid_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")


# ✅ Task A4: Sort Contacts
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
        
        return f"✅ Sorted contacts successfully saved to {output_path}"
    
    except Exception as e:
        return f"Error sorting JSON: {str(e)}"


# ✅ Task A5: Extract Credit Card Number
def extract_credit_card_number(image_path: str, output_path: str):
    """Extracts the credit card number from an image using OCR."""
    
    if not os.path.exists(image_path):
        return f"Error: Image {image_path} not found."

    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)

        credit_card_number = re.search(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b", extracted_text)
        if credit_card_number:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(credit_card_number.group(0).replace(" ", "").replace("-", ""))
            return f"✅ Credit card number extracted and saved to {output_path}"
        else:
            return "No credit card number found in the image."
    
    except Exception as e:
        return f"Error processing image: {str(e)}"
    
    
    # ✅ Ensure the function is defined
# def create_markdown_index(directory_path: str, output_path: str):
#     """Creates an index of Markdown files with their first H1 title."""
    
#     if not os.path.exists(directory_path):
#         return f"Error: Directory {directory_path} not found."

#     md_files = []
#     for root, _, files in os.walk(directory_path):
#         for file in files:
#             if file.endswith(".md"):
#                 relative_path = os.path.relpath(os.path.join(root, file), directory_path)
#                 md_files.append(relative_path)

#     index = {}
#     for md_file in md_files:
#         full_path = os.path.join(directory_path, md_file)
#         with open(full_path, "r", encoding="utf-8") as f:
#             for line in f:
#                 if line.startswith("# "):
#                     title = line.strip("# ").strip()
#                     index[md_file] = title
#                     break  

#     try:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(index, f, indent=4)
#         return f"✅ Markdown index created at {output_path}"
#     except Exception as e:
#         return f"Error writing index file: {str(e)}"


def create_markdown_index(directory_path: str, output_path: str):
    """
    Creates an index of Markdown files with their first H1 title.
    Args:
        directory_path (str): Path to the directory containing Markdown files.
        output_path (str): Path to save the index JSON file.
    Returns:
        str: Success or error message.
    """
    # if not os.path.exists(directory_path):
    #     return f"Error: Directory {directory_path} not found."


    directory_path = os.path.abspath(directory_path) + "/"  # Ensure trailing slash
    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} not found."

    index = {}
    for file in os.listdir(directory_path):
        if file.endswith(".md"):
            with open(os.path.join(directory_path, file), "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# "):
                        index[file] = line.strip("# ").strip()
                        break

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    return f"Markdown index created at {output_path}"

def get_recent_logs(directory_path: str, output_path: str):
    """Writes the first line of the 10 most recent .log files to a file."""
    # if not os.path.exists(directory_path):
    #     return f"Error: Directory {directory_path} not found"

    directory_path = os.path.abspath(directory_path) + "/"  # Ensure trailing slash
    if not os.path.exists(directory_path):
        return f"Error: Directory {directory_path} not found."

    log_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".log")]
    log_files.sort(key=os.path.getmtime, reverse=True)

    recent_logs = log_files[:10]
    first_lines = []
    for log_file in recent_logs:
        with open(log_file, "r", encoding="utf-8") as f:
            first_lines.append(f.readline().strip())

    write_to_file(output_path, "\n".join(first_lines))
    return f"✅ First lines of 10 most recent logs written to {output_path}"