from controllers.auth_controller import update_profile_image
from middleware.auth_middleware import verify_token
from fastapi import Depends
from fastapi import APIRouter, UploadFile, File
import shutil
from database import users
router = APIRouter()

# @router.post("/upload")
# def upload_file(file: UploadFile = File(...)):

#     with open(f"uploads/{file.filename}", "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {
#         "message": "File Uploaded Successfully",
#         "filename": file.filename
#     }
@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    user=Depends(verify_token)
):

    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_path = f"uploads/{file.filename}"

    update_profile_image(
        user["email"],
        image_path
    )

    return {
        "message": "Profile Image Uploaded",
        "image": image_path
    }

def update_profile_image(email, image_path):

    result = users.update_one(
        {"email": email},
        {
            "$set": {
                "profile_image": image_path
            }
        }
    )

    user = users.find_one({"email": email})

    print(user)

    return {
        "message": "Profile Image Updated"
    }

