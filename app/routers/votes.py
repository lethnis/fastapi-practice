from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .oauth2 import get_current_user
from ..models import UserTable, VotesTable, PostTable
from ..database import get_db
from ..schemas import UserCreate, UserResponse, VoteAction
from ..utils import hash_password

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteAction, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    post = db.query(PostTable).filter(PostTable.id == vote.post_id).first()

    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {vote.post_id} not found")

    vote_query = db.query(VotesTable).filter(VotesTable.post_id == vote.post_id, VotesTable.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.direction == 1:

        if found_vote is not None:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, f"User {current_user.id} has already voted on post {vote.post_id}"
            )

        new_vote = VotesTable(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    elif vote.direction == 0:
        if found_vote is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "you can't unlike post you didn't like in the first place")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
