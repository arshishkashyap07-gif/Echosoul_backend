
from fastapi import APIRouter, HTTPException
from auth.auth_models import RegisterModel, LoginModel
from auth.auth_utils import hash_password, verify_password, create_token
from database import users_collection

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: RegisterModel):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
    })
    return {"message": "Registration successful"}

@router.post("/login")
def login(user: LoginModel):
    db_user = users_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {"access_token": token}
