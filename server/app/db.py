"""Файл с настройками для базы данных."""

from tortoise.contrib.fastapi import register_tortoise

from app.config import (
    db_url,
    generate_schemas,
    add_exception_handlers,
    models
)


def init(app):
    """Функция для инициализации базы данных."""
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": models},
        generate_schemas=generate_schemas,
        add_exception_handlers=add_exception_handlers,
    )
