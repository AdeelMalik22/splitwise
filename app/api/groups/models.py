import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from app.utils.database_connections import Base


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100),unique=False, nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class UsersGroups(Base):
    __tablename__ = "users_groups"
    id = Column(Integer, primary_key=True,autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

