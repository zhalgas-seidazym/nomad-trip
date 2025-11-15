from fastapi import FastAPI

from src.presentation.v1.routers import user_router


app = FastAPI()

app.include_router(user_router.router)