# type: ignore
import uuid

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from sqlalchemy import JSON, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)
