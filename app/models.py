from .db import Base
from sqlalchemy import Column, Integer, String,Boolean,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Reference posts relationship
    # posts = relationship("Post", back_ref="owner")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False,default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    # Reference User relationship
    # owner = relationship("User", back_populates="posts")

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {"schema": "public"}

    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("public.posts.id", ondelete="CASCADE"), primary_key=True)

