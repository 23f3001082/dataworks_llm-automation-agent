from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback
from api.file_manager import read_file
from api.task_processor import execute_task

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LLM Automation Agent is Running 🚀"}

@app.get("/read")
def read_data(path: str):
    """Endpoint to read a file from the /data directory."""
    try:
        content = read_file(path)
        return {"status": "success", "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not Found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Access outside /data/ is restricted.")
    except Exception as e:
        print("Error:", traceback.format_exc())  # Debugging logs
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Define a Pydantic model for the JSON request
class TaskRequest(BaseModel):
    task: str

@app.post("/run")
def run_task(request: TaskRequest):
    """Endpoint to execute a plain-English task request."""
    task_description = request.task

    if not task_description:
        raise HTTPException(status_code=400, detail="Task description is required")

    try:
        result = execute_task(task_description)
        return {"status": "success", "result": result}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        print("Error:", traceback.format_exc())  # Debugging logs
        raise HTTPException(status_code=500, detail="Internal Server Error")