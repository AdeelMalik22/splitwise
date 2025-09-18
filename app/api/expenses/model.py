import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from app.utils.database_connections import Base


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100),unique=False, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    description = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    paid_by = Column(ARRAY(Integer), nullable=False)
    split_on = Column(ARRAY(Integer), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

