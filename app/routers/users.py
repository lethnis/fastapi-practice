from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..models import UserTable
from ..database import get_db
from ..schemas import UserCreate, UserResponse
from ..utils import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash the password
    user.password = hash_password(user.password)

    user = UserTable(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    return user
