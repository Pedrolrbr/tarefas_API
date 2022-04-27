from datetime import date, datetime
from sqlite3 import Date
from sqlalchemy import DATE, Boolean, Column, Integer, String


from .database import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id          = Column(Integer, primary_key=True, index=True)
    tipo        = Column(String)
    title       = Column(String)
    complete    = Column(Boolean, default=False)
    dia         = Column(String)



