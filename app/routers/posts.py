from typing import List, Union
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .oauth2 import get_current_user
from ..models import PostTable, VotesTable
from ..database import get_db
from ..schemas import PostCreate, PostUpdate, PostResponse, PostVote

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostVote])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: str = "",
):
    posts_votes = (
        db.query(PostTable, func.count(VotesTable.post_id).label("votes"))
        .join(VotesTable, VotesTable.post_id == PostTable.id, isouter=True)
        .group_by(PostTable.id)
        .order_by(PostTable.id)
        .filter(PostTable.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )

    return [{"Post": i[0], "votes": i[1]} for i in posts_votes]


# @router.get("/posts/latest")
# def get_latest_post():
#     return {"data": my_posts[-1]}


@router.get("/{id}", response_model=PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    post = (
        db.query(PostTable, func.count(VotesTable.post_id).label("votes"))
        .join(VotesTable, VotesTable.post_id == PostTable.id, isouter=True)
        .group_by(PostTable.id)
        .filter(PostTable.id == id)
        .first()
    )

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return {"Post": post[0], "votes": post[1]}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = PostTable(user_id=current_user.id, **post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    post = db.query(PostTable).filter(PostTable.id == id)

    if post.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": f"Not found post with id {id}"})

    if post.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"message": "You can't delete others peoples posts"})

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):

    post_query = db.query(PostTable).filter(PostTable.id == id)

    if post_query.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": f"Not found post with id {id}"})

    if post_query.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"message": "what are you think you're doing?"})

    post_query.update(post.model_dump())
    db.commit()

    return post_query.first()
