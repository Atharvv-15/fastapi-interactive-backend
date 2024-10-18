from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Post 1", "content": "Post 1 content", "id": 1}]

@app.get("/")
def read_root():
    return {"message": "Learning python"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post_dict)
    return {"data": my_posts}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return {f"post_details: {post}"}

def find_id(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_id(id) 

    if index == None:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with the {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)