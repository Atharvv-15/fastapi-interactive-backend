from fastapi import FastAPI, Response, status, HTTPException
from . import models
from .db import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .utils import hash
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
#Create all the tables in the database
#This is done by alembic automatically, but we can also do it manually like this ,so for now we will not use it9:
# models.Base.metadata.create_all(bind=engine)

# Explicitly initialize models in correct order
from .models import User, Post, Vote

app = FastAPI()

origins = ["*"]

# Force model registration before setting up middleware and routers
# Add this line to reflect existing tables
# models.Base.metadata.create_all(bind=engine) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include the user router
app.include_router(user.router)

#Include the post router
app.include_router(post.router)

#Include the auth router
app.include_router(auth.router)

#Include the vote router
app.include_router(vote.router)

#Root route
@app.get("/")
def read_root():
    return {"message": "Learning python API and Pushing the code to Ubuntu server using github actions"}







