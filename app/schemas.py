from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
#Create a Post response schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#Create a Post response schema
class PostCreate(PostBase):
    pass
        
#Create a Post response schema
class PostResponse(PostBase):
    id: int
    created_at: datetime

#Create a Post update schema
class PostUpdate(BaseModel):
    title: Optional[str] = "no title"
    content: Optional[str] = "no content"
    published: Optional[bool] = True

#Create a User schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Create a User response schema
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

#Create a Login user schema
class LoginUser(BaseModel):
    email: EmailStr
    password: str

