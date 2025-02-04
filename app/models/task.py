from sqlalchemy import Column, String, DateTime, Enum
from app.database import Base
import uuid
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum("pendiente", "en_progreso", "completada", name="status_enum"), default="pendiente")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
