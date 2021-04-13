from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ShowBlog, Blog, User
from .. import models
from ..oauth2 import get_current_user


router = APIRouter(prefix="/blog", tags=["Blogs"])

@router.get('/', response_model=List[ShowBlog])
def get_blogs(db: Session=Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
  blogs = db.query(models.Blog).all()
  return blogs


@router.get('/{id}', response_model=ShowBlog)
def get_blog(id: int, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if blog:
    return blog
  else:
    raise HTTPException(status_code=404, detail=f"Blog with id {id} not found.")


@router.post('/', status_code = 201)
def create_blog(req: Blog, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
  new_blog = models.Blog(title=req.title, body=req.body, user_id=req.user_id)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return {"detail": "Successfully created blog post", "new blog": new_blog}


@router.put('/{id}', status_code = 202)
def update_blog(id: int, req: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if blog:
    db.query(models.Blog).filter(models.Blog.id == id).update({"title":req.title, "body":req.body, "user_id":req.user_id})
    db.commit()
    return {"detail": f"Successfuly updated blog with id {id}", "updated blog": req}
  else:
    raise HTTPException(status_code=404, detail=f"Blog with id {id} not found.")


@router.delete('/{id}', status_code = 204)
def delete_blog(id: int, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if blog:
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {"detail": f"Blog at id {id} deleted."}
  else:
    raise HTTPException(status_code=404, detail=f"Blog with id {id} not found.")