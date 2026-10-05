from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models
from .cache import cache_tasks, clear_task_cache, get_cached_tasks
from .database import Base, engine, get_db
from .schemas import TaskCreate, TaskResponse


app = FastAPI(
    title="Kubernetes Learning Task API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend",
    }


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    cached = get_cached_tasks()

    if cached is not None:
        return cached

    tasks = db.query(models.Task).order_by(models.Task.id.desc()).all()

    result = [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }
        for task in tasks
    ]

    cache_tasks(result)

    return result


@app.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty",
        )

    new_task = models.Task(
        title=task.title.strip(),
        completed=False,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    clear_task_cache()

    return new_task


@app.put("/tasks/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    task.completed = not task.completed

    db.commit()
    db.refresh(task)

    clear_task_cache()

    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    clear_task_cache()

    return {
        "message": "Task deleted",
    }