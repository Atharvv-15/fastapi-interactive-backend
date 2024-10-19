from fastapi import FastAPI, Response, status, HTTPException
from . import models
from .db import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .utils import hash
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Include the post router
app.include_router(post.router)

#Include the user router
app.include_router(user.router)

#Include the auth router
app.include_router(auth.router)

#Root route
@app.get("/")
def read_root():
    return {"message": "Learning python"}







