from typing import Optional
from random import randrange
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "first title", "content": "content of first title", "id": 1},
    {"title": "second title", "content": "content of second title", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get('/')
def root():
    return {"messages": "Hello World!"}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}


@app.post('/posts')
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post.dict())
    return {
        "data": post_dict
    }


@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    return {"post": post}
