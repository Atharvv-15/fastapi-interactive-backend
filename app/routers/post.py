from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db
from ..schemas import PostCreate, PostResponse, PostUpdate

#Create a post router
router = APIRouter(prefix="/posts", tags=["Posts"])

#Get all posts
@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Get a post
@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    return post

#Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with the {id} does not exist")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update a post
@router.put("/update/{id}", response_model=PostResponse) 
def update_post(id:int,post:PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with the {id} does not exist")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {post_query.first()}