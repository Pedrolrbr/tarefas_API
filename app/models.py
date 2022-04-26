from datetime import date, datetime
from numpy import datetime_as_string
from sqlalchemy import DATE, Boolean, Column, Integer, String


from .database import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    complete    = Column(Boolean, default=False)
    dia         = Column(Integer)

