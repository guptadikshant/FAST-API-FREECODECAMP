from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get('/')
def root():
    return {"messages": "Hello World!"}


@app.get('/post')
def get_posts():
    return {"data": "this is your post"}


@app.post('/createposts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {
        "title": payload["title"],
        "content": payload["content"]
    }
