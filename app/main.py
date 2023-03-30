from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.schemas import Post, PostCreate, UserCreate, UserOut
from app.utils import hash


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


@app.get('/')
def root():
    return {"messages": "Hello World!"}


@app.get('/posts', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    post_dict = post.dict()
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found for id {id}")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    posts = updated_post.first()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

