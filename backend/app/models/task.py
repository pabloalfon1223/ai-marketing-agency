from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    agent_type = Column(String(50), nullable=False)
    task_type = Column(String(100), nullable=False)
    input_data = Column(Text)  # JSON
    output_data = Column(Text)  # JSON
    status = Column(String(20), default="pending")  # pending | running | completed | failed
    priority = Column(Integer, default=5)  # 1=highest, 10=lowest
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    error_message = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="tasks")
    campaign = relationship("Campaign", back_populates="tasks")
    parent_task = relationship("Task", remote_side="Task.id", backref="subtasks")
    logs = relationship("AgentLog", back_populates="task", cascade="all, delete-orphan")
