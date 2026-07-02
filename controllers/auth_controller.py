from database import users
from models.user_model import User
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET")


def signup(user: User):

    existing = users.find_one({"email": user.email})

    if existing:
        return {"message": "Email already exists"}

    hashed_password = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    )

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }

    users.insert_one(new_user)

    return {"message": "Signup Successful"}


def login(email, password):

    user = users.find_one({"email": email})

    if not user:
        return {"message": "User not found"}

    if not bcrypt.checkpw(
        password.encode(),
        user["password"]
    ):
        return {"message": "Wrong Password"}

    token = jwt.encode(
        {"email": user["email"]},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Login Successful",
        "token": token
    }