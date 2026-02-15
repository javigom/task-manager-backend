from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud, auth, models
from ..db import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.TaskRead)
async def create_task(task_in: schemas.TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(auth.get_current_user)):
    task = await crud.create_task(db, current_user.id, task_in.title, task_in.description)
    return task


@router.get("/", response_model=List[schemas.TaskRead])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    """List tasks for current user with pagination."""
    tasks = await crud.list_tasks_for_user(db, current_user.id, skip=skip, limit=limit)
    return tasks


@router.post("/{task_id}/participants")
async def add_participant(task_id: int, email: str, db: AsyncSession = Depends(get_db), current_user=Depends(auth.get_current_user)):
    q = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = q.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only task owner can add participants")
    user = await crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = await crud.add_participant(db, task, user)
    return {"status": "ok", "task_id": task.id}
