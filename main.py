from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for tasks
tasks = []
task_id_counter = 1

# Task Model
class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

# API Endpoints

@app.get("/")
def home():
    return {"message": "Welcome to Task Manager API!"}

@app.post("/tasks/")
def create_task(task: Task):
    global task_id_counter
    new_task = {"id": task_id_counter, **task.dict()}
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.get("/tasks/")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_task.dict())
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return {"message": "Task deleted successfully"}
