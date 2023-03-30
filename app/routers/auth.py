from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin
from app import models, utils, outh2


router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    # if the entered password and password already stored does not match
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    access_token = outh2.create_access_token(data={"user_id": user.id})
    

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }