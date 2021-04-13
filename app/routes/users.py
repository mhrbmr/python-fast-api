from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ShowUser, SimpleUserInfo, User as UserSchema
from ..models import User as UserModel
from ..hashing import Hash
from ..oauth2 import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.get('/', response_model=List[ShowUser])
def get_users(db: Session=Depends(get_db), current_user: UserSchema = Depends(get_current_user)) -> dict:
  users = db.query(UserModel).all()
  return users


@router.get('/{id}', response_model=ShowUser)
def get_user(id: int, db: Session=Depends(get_db), current_user: UserSchema = Depends(get_current_user)) -> dict:
  user = db.query(UserModel).filter(UserModel.id == id).first()
  if user:
    return user
  else:
    raise HTTPException(status_code=404, detail=f"User with id {id} not found.")


@router.post('/', status_code=201, response_model=SimpleUserInfo)
def create_user(req: UserSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)) -> dict:
  new_user = UserModel(name=req.name, email=req.email, password=Hash.bcrypt(req.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user