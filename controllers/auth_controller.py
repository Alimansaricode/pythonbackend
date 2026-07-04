from database import users
from models.user_model import User
import bcrypt
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

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


# def login(email, password):

#     user = users.find_one({"email": email})

#     if not user:
#         return {"message": "User not found"}

#     if not bcrypt.checkpw(
#         password.encode(),
#         user["password"]
#     ):
#         return {"message": "Wrong Password"}

#     token = jwt.encode(
#         {"email": user["email"]},
#         SECRET_KEY,
#         algorithm="HS256"
#     )

#     return {
#         "message": "Login Successful",
#         "token": token
#     }
def login(email, password):

    user = users.find_one({"email": email})

    if not user:
        return {"message": "User not found"}

    if not bcrypt.checkpw(
        password.encode(),
        user["password"]
    ):
        return {"message": "Wrong Password"}

    access_payload = {
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    refresh_payload = {
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    access_token = jwt.encode(
        access_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        refresh_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def update_user(email, name):
    users.update_one(
        {"email": email},
        {"$set": {"name": name}}
    )

    return {"message": "Profile Updated"}

def delete_user(email):
    users.delete_one(
        {"email": email}
    )

    return {"message": "Account Deleted"}

def refresh_access_token(refresh_token):

    try:
        data = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        payload = {
            "email": data["email"],
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }

        access_token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "access_token": access_token
        }

    except:
        return {
            "message": "Invalid Refresh Token"
        }