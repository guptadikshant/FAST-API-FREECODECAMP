from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models,outh2
from app.schemas import Post, PostCreate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get('/', response_model=List[Post])
def get_posts(db: Session = Depends(get_db),
              current_user:int = Depends(outh2.get_current_user),
              limit:int=10):
    """
    Request to get all posts
    """
    posts = db.query(models.Post).limit(limit).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user:int = Depends(outh2.get_current_user)):
    """
    Request to create a new post
    """
    post_dict = post.dict()
    new_post = models.Post(owner_id=current_user.id,**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=Post)
def get_post(id: int, response: Response, 
             db: Session = Depends(get_db),
             current_user:int = Depends(outh2.get_current_user)):
    """
    Request to get a single post
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found for id {id}")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db),
                current_user:int = Depends(outh2.get_current_user)):
    """
    Request to delete a post
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform the action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, 
                post: PostCreate, 
                db: Session = Depends(get_db), 
                current_user:int = Depends(outh2.get_current_user)):
    """
    Request to update a post
    """
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    posts = updated_post.first()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform the action")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()