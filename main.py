# from fastapi.openapi.utils import get_openapi
# from fastapi import FastAPI
# from routes.auth_routes import router #FastAPI framework को import करना।


# app = FastAPI() #FastAPI framework को import करना।

# app.include_router(router)

# app.include_router(router) #routes/auth_routes.py से सारे routes import करना। @router.post("/signup")
from fastapi import FastAPI
from routes.auth_routes import router
from routes.upload_routes import router as upload_router

app = FastAPI()

# Authentication Routes
app.include_router(router)

# Upload Routes
app.include_router(upload_router)