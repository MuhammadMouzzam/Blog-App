from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from main_folder.database import Base

class Blogs(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable= True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)
    created_at = Column(TIMESTAMP(timezone=True) , server_default=text('now()'), nullable=False)

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key = True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , server_default=text('now()'))
    blog_id = Column(Integer, ForeignKey('blogs.id', ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

class Vote(Base):
    __tablename__ = 'votes'
    
    blog_id = Column(Integer, ForeignKey('blogs.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)