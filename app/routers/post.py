from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas
from ..db import get_db
from ..schemas import PostCreate, PostResponse, PostUpdate,PostResponseWithVotes
from ..oauth2 import get_current_user
from sqlalchemy import func
#Create a post router
router = APIRouter(prefix="/posts", tags=["Posts"])

#Add dependencies to all the posts routes: User should be authenticated to access the posts

#Get all posts
@router.get("/", response_model=list[PostResponseWithVotes])
#If we want to get all posts for the current user,while being authenticated, we can use the following route:
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
def get_posts(db: Session = Depends(get_db) , limit :int = 10, skip:int = 0,search:Optional[str] = ""):
    
    #Get all posts from the database
    #We can also add a limit to the number of posts we want to get, and a skip to skip a certain number of posts, 
    #and a search to search for a certain post
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #Get all posts with votes
    #Here we are joining the Post and Vote models, and we are grouping the results by the post id, and we are filtering the results by the search query
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
            models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #Only get all posts for the current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

#Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    #Added dependency to get the current user before creating a post    
    #Add the owner_id to the post, as it is a required field in the Post model and a foreign key to the User model: user_id
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Get a post
@router.get("/{id}", response_model=PostResponseWithVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
            models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    
    #Check if the post owner is the same as the current user
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return post

#Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with the {id} does not exist")
    
    #Check if the post owner is the same as the current user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT , content="Post deleted successfully")

#Update a post
@router.put("/update/{id}", response_model=PostResponse) 
def update_post(id:int,post:PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with the {id} does not exist")
    
    #Check if the post owner is the same as the current user
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post
