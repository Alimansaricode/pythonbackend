from fastapi import APIRouter, Depends
from models.user_model import User
from models.login_model import LoginUser
from controllers.auth_controller import signup, login
from middleware.auth_middleware import verify_token

router = APIRouter()


@router.post("/signup")
def register(user: User):
    return signup(user)


@router.post("/login")
def authenticate(user: LoginUser):
    return login(user.email, user.password)


@router.get("/profile")
def profile(user=Depends(verify_token)):
    return {
        "message": "Protected Route",
        "user": user
    }

@router.get("/me")
def get_current_user(user=Depends(verify_token)):
    return {
        "message": "Current User",
        "user": user
    }


@router.put("/update-profile")
def update_profile(user=Depends(verify_token)):
    return {
        "message": "Profile Updated",
        "user": user
    }


@router.delete("/delete-account")
def delete_account(user=Depends(verify_token)):
    return {
        "message": "Account Deleted",
        "user": user
    }