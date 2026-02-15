from __future__ import with_statement
import app.db as app_db
from app.config import settings as app_settings
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

import asyncio
import os
import sys
from pathlib import Path
from logging.config import fileConfig

# Ensure src directory is on sys.path so `import app` works (src layout)
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = app_db.Base.metadata


def get_url() -> str:
    return (
        os.environ.get("DATABASE_URL")
        or config.get_main_option("sqlalchemy.url")
        or getattr(app_settings, "DATABASE_URL", None)
    )


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    url = get_url()
    if not url:
        raise RuntimeError(
            "No database URL configured for Alembic. Set the DATABASE_URL env var or add `sqlalchemy.url` to alembic.ini.`"
        )

    connectable = create_async_engine(url, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
