import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context
from app import models

load_dotenv(".env")
LOCAL_ENV = os.getenv("ENV")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

cmd_kwargs = context.get_x_argument(as_dictionary=True)
if "env" not in cmd_kwargs:
    raise Exception(
        "We couldn't find `env` in the CLI arguments. "
        "Please verify `alembic` was run with `-x db=<db_name>` "
        "(e.g. `alembic -x env=dev upgrade head`)"
    )
target_environment = cmd_kwargs["env"]
if target_environment != LOCAL_ENV:
    r = input(
        "You are targeting an environment that mismatches your local environment. Continue?\n[y/N]: "
    )
    if r.lower() != "y":
        print("Aborting")
        exit(1)
env_variable = {"dev": "DATABASE_URL", "prod": "DATABASE_URL_PROD"}[target_environment]

# Configuring the database url
database_url = os.getenv(env_variable)
print(f"Using database url {database_url}")
if database_url is None:
    raise ValueError(f"{database_url} is not set")
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = models.Base.metadata


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
