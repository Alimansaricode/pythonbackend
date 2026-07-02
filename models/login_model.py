from pydantic import BaseModel


class LoginUser(BaseModel):
    email: str
    password: str

    # Login body validate करता है।  step 3 