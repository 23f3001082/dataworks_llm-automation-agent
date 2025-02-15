import os
import subprocess
import json
from api.llm_handler import parse_task
from api.utils import execute_shell, read_json, write_to_file
from api.file_manager import list_files
from api.utils import execute_shell


def execute_task(task_description: str):
    parsed_task = parse_task(task_description)

    if "install uv and run datagen.py" in parsed_task:
        return execute_shell("pip install uv && python datagen.py user@example.com")
    elif "format markdown" in parsed_task:
        return execute_shell("npx prettier@3.4.2 --write /data/format.md")
    elif "count Wednesdays" in parsed_task:
        return count_weekdays("/data/dates.txt", "Wednesday")
    elif "sort contacts" in parsed_task:
        return sort_json("/data/contacts.json", "/data/contacts-sorted.json")
    elif "extract sender email" in parsed_task:
        return extract_email("/data/email.txt")
    if "install uv and run datagen.py" in task_description.lower():
        return execute_shell("pip install uv && python datagen.py user@example.com")
    elif "format markdown" in task_description.lower():
        return execute_shell("npx prettier@3.4.2 --write /data/format.md")
    elif "count Wednesdays" in task_description.lower():
        return execute_shell("grep -i Wednesday /data/dates.txt | wc -l > /data/dates-wednesdays.txt")
    else:
        raise ValueError("Task not recognized")
    

def count_weekdays(file_path, weekday):
    with open(file_path, 'r') as f:
        dates = f.readlines()
    count = sum(1 for date in dates if weekday in date)
    write_to_file(f"{file_path[:-4]}-wednesdays.txt", str(count))
    return f"Counted {count} {weekday}s"