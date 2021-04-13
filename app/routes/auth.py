from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..schemas import Login
from ..database import get_db
from ..models import User
from ..hashing import Hash
from ..token import create_access_token


router = APIRouter(tags=["Auth"])

@router.post('/login')
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
  user = db.query(User).filter(User.email == req.username).first()
  if not user:
    raise HTTPException(status_code=401, detail="Incorrect email or password, please try again.")
  if not Hash.verify(req.password, user.password):
    raise HTTPException(status_code=401, detail="Incorrect email or password, please try again.")
  if Hash.verify(req.password, user.password):
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}