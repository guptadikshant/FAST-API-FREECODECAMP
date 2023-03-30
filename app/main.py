from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.database import engine
from app.routers import post, users,auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='Dikshant1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established.")
        break

    except Exception as e:
        print("Connection error")
        print(f"Error : {e}")
        time.sleep(2)


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)




@app.get('/')
def root():
    return {"messages": "Hello World!"}



