from fastapi import status,HTTPException,Depends,APIRouter
from .. import schemas,models,oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func

router=APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)|models.Post.content.contains(search)).limit(limit).offset(skip).all()
    #posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)|models.Post.content.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.dict())             #(title=post.title,content=post.content,published=post.published))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found.")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to perform the operation.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"Details":"Post successfully deleted."}


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostUpdate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    query_post=db.query(models.Post).filter(models.Post.id==id)
    get_post=query_post.first()
    if get_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found.")
    if get_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to perform the operation.")
    query_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return get_post


