from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.api.groups.models import UsersGroups, Groups
from app.api.users.models import User
from app.api.users.schema.request import CreateUsers, UpdateUser, LoginRequest
from app.api.users.schema.response import UserResponseData
from app.utils.auth import authenticate_user, get_current_user
from app.utils.database_connections import get_db
from app.utils.hash_password import create_access_token, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/api/v1/login")
def login(login_data: LoginRequest,db: Session = Depends(get_db)):
    """Generate Access Token"""
    user = db.query(User).filter(User.username == login_data.username).first()
    if user:
        user_response =  authenticate_user(login_data.password,user)
        token_data = {"sub":user_response.username}
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )



@router.post("/creat_users", response_model=UserResponseData)
def create_user(request:CreateUsers,db:Session= Depends(get_db)):
    email_validation = db.query(User).filter(User.email == request.email).first()
    if email_validation:
        raise HTTPException("Email already registered")
    username_validation = db.query(User).filter(User.username == request.username).first()
    if username_validation:
        raise HTTPException("Username already taken")

    hashed_password = get_password_hash(request.password)
    user_dict = request.dict()
    user_dict["password"] = hashed_password
    user = User(name=request.name, email=request.email,age=request.age,username=request.username,password=user_dict.get("password"))
    db.add(user)
    db.commit()
    return user


@router.get("/get_user", response_model=list[UserResponseData])
def get_users(db:Session= Depends(get_db),user=Depends(get_current_user)):
    users = db.query(User).all()
    if users:
        return users
    return {"message": "No users found"}

@router.put("/update_user")
def update_user(request:UpdateUser,db:Session= Depends(get_db),user=Depends(get_current_user)):
    user = db.query(User).filter(User.username == user).first()
    if user:
        if request.name is not None:
            user.name = request.name
        if request.email is not None:
            user.email = request.email
        if request.age is not None:
            user.age = request.age
        if request.username is not None:
            user.username = request.username

        db.commit()
        db.refresh(user)

        return {"message": "User updated successfully"}
    return {"message": "No user found"}


@router.delete("/delete_user/{user_id}")
def delete_users(user_id:int,db:Session= Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "No user found"}


@router.get("/{user_id}")
def get_groups_by_user_id(user_id:int,db:Session= Depends(get_db)):
    groups_ids =db.query(UsersGroups).filter(UsersGroups.user_id == user_id).all()
    user_gropus = []
    if groups_ids:
        for ids in groups_ids:
            groups = db.query(Groups).filter(Groups.id == ids.group_id).first()
            user_gropus.append(groups)
    return user_gropus

@router.delete("left_group/{group_id}")
def delete_group(group_id:int,db:Session= Depends(get_db),user = Depends(get_current_user)):
    remove_group = db.query(UsersGroups).filter(UsersGroups.group_id == group_id,UsersGroups.user_id==user[1]).first()
    if remove_group:
        db.delete(remove_group)
        db.commit()
        return {"message": "Group deleted successfully"}
    return {"message": "No group found"}