from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated
#Create a User schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Create a User response schema
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

#Create a Login user schema
class LoginUser(BaseModel):
    email: EmailStr
    password: str

#Create a Post response schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True

#Create a Post response schema
class PostCreate(PostBase):
    pass

    class Config:
        orm_mode = True


#Create a Post response schema
class PostResponse(PostBase):
    title: str
    content: str
    published: bool
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

#Create a Post response schema with votes
class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

#Create a Post update schema
class PostUpdate(BaseModel):
    title: Optional[str] = "no title"
    content: Optional[str] = "no content"
    published: Optional[bool] = True

#Create a Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

#Create a Token payload schema
class TokenPayload(BaseModel):
    user_id: Optional[int] = None

#Create a Vote schema
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]

