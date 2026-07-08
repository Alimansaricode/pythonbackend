from controllers.auth_controller import get_profile
from fastapi import APIRouter, Depends
from models.user_model import User
from models.login_model import LoginUser
from controllers.auth_controller import signup, login
from middleware.auth_middleware import verify_token
from models.update_model import UpdateUser
from controllers.auth_controller import update_user
from controllers.auth_controller import delete_user
from models.refresh_model import RefreshToken
from controllers.auth_controller import refresh_access_token
from controllers.auth_controller import logout
from controllers.auth_controller import get_all_users
router = APIRouter()


@router.post("/signup")
def register(user: User):
    return signup(user)


@router.post("/login")
def authenticate(user: LoginUser):
    return login(user.email, user.password)


# @router.get("/profile")
# def profile(user=Depends(verify_token)):
#     return {
#         "message": "Protected Route",
#         "user": user
#     }
@router.get("/profile")
def profile(user=Depends(verify_token)):
    return get_profile(user["email"])

@router.get("/me")
def get_current_user(user=Depends(verify_token)):
    return {
        "message": "Current User",
        "user": user
    }


# @router.put("/update-profile")
# def update_profile(user=Depends(verify_token)):
#     return {
#         "message": "Profile Updated",
#         "user": user
#     }
@router.put("/update-profile")
def update_profile(
    data: UpdateUser,
    user=Depends(verify_token)
):
    return update_user(
        user["email"],
        data.name
    )

# @router.delete("/delete-account")
# def delete_account(user=Depends(verify_token)):
#     return {
#         "message": "Account Deleted",
#         "user": user
#     }
@router.delete("/delete-account")
def delete_account(
    user=Depends(verify_token)
):
    return delete_user(user["email"])

@router.post("/refresh")
def refresh(data: RefreshToken):
    return refresh_access_token(data.refresh_token)

@router.post("/logout")
def logout():
    return logout()

@router.get("/users")
def all_users(user=Depends(verify_token)):
    return get_all_users()