from fastapi import FastAPI, HTTPException
from api.task_processor import execute_task
from api.file_manager import read_file

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    try:
        result = execute_task(task)
        return {"status": "success", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/read")
async def read_data(path: str):
    try:
        content = read_file(path)
        return {"status": "success", "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not Found")