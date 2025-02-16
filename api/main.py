from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import traceback
import os
from api.file_manager import read_file
from api.task_processor import execute_task, count_weekdays

app = FastAPI()

# Define the base directory for resolving file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

@app.get("/")
def home():
    return {"message": "LLM Automation Agent is Running 🚀"}

@app.get("/read")
def read_data(path: str = Query(..., description="Path of the file to read")):
    """Reads a file from the /data directory."""
    
    full_path = os.path.join(BASE_DIR, os.path.basename(path))  # Prevent directory traversal
    print(f"DEBUG: Requested file path - {full_path}")

    try:
        content = read_file(full_path)
        return {"status": "success", "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not Found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Access outside /data/ is restricted.")
    except Exception as e:
        print("ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

class TaskRequest(BaseModel):
    task: str

@app.post("/run")
async def run_task(task: str = Query(..., description="Plain-English task description")):
    """Executes a plain-English task request provided as a query parameter."""
    task_description = task.strip()
    print(f"DEBUG: Received Task - {task_description}")

    if not task_description:
        raise HTTPException(status_code=400, detail="Task description is required")

    try:
        if "count" in task_description.lower():
            words = task_description.split()
            if len(words) >= 2:  # Ensure valid input
                weekday = words[1]  # e.g., "Monday" from "Count Monday"
                result = count_weekdays(os.path.join(BASE_DIR, "dates.txt"), weekday)
            else:
                raise ValueError("Invalid format. Use 'Count <Weekday>'")
        else:
            result = execute_task(task_description)

        print(f"DEBUG: Task Execution Result - {result}")
        return {"status": "success", "result": result}

    except ValueError as e:
        print(f"ERROR: Invalid Task - {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print("ERROR: Unexpected Failure:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")