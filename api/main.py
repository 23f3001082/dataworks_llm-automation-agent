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
def read_data(path: str):
    """Endpoint to read a file from the /data directory."""
    
    print(f"DEBUG: path - {path}")
    print(f"DEBUG: BASE_DIR - {BASE_DIR}")

    try:
        content = read_file(path)
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
        # Extract weekday dynamically (e.g., "Count Monday")
        words = task_description.split()
        if len(words) >= 2 and words[0].lower() == "count":
            weekday = words[1]  # Extract "Monday" from "Count Monday"
            if weekday.capitalize() in [
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
            ]:
                result = count_weekdays(os.path.join(BASE_DIR, "dates.txt"), weekday)
            else:
                raise ValueError("Invalid weekday. Use a valid day name (e.g., Monday)")
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