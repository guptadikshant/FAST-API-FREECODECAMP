from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root():
    return {"messages": "Hello World!"}


@app.get('/post')
def get_posts():
    return {"data": "this is your post"}
