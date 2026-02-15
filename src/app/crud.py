from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    q = await db.execute(select(models.User).where(models.User.email == email))
    return q.scalars().first()


async def create_user(db: AsyncSession, email: str, hashed_password: str, full_name: str | None = None) -> models.User:
    user = models.User(
        email=email, hashed_password=hashed_password, full_name=full_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_task(db: AsyncSession, owner_id: int, title: str, description: str | None = None) -> models.Task:
    task = models.Task(title=title, description=description, owner_id=owner_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def list_tasks_for_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Task]:
    """List tasks for a user with pagination."""
    q = await db.execute(
        select(models.Task)
        .where(models.Task.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(models.Task.created_at.desc())
    )
    return q.scalars().all()


async def add_participant(db: AsyncSession, task: models.Task, user: models.User) -> models.Task:
    task.participants.append(user)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
