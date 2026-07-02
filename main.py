from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from routes.auth_routes import router #FastAPI framework को import करना।

app = FastAPI() #FastAPI framework को import करना।

app.include_router(router) #routes/auth_routes.py से सारे routes import करना। @router.post("/signup")