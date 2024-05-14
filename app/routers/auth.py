from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .oauth2 import create_access_token
from ..database import get_db
from ..schemas import UserLogin, Token
from ..models import UserTable
from ..utils import verify

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(UserTable).filter(UserTable.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email not found")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")

    # create a token
    # return the token
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
