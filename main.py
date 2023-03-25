from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root():
    return {"messages": "Hello World!"}
