from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base, engine

class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    task = Column(String(255))
    status = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)    