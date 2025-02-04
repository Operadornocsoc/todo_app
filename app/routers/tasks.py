from fastapi import APIRouter, HTTPException
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.database import SessionLocal

router = APIRouter()

@router.get("/tasks/")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks/")
def create_task(task: TaskCreate):
    db = SessionLocal()
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@router.put("/tasks/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    db = SessionLocal()
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    db.close()
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    db = SessionLocal()
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    db.close()
    return {"message": "Task deleted"}
