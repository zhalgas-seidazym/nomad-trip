from fastapi import FastAPI

from src.presentation.v1.routers import user_router, admin_router, company_router
from .container import Container


container = Container()
app = FastAPI()
app.container = container


app.include_router(admin_router.router)
app.include_router(user_router.router)
app.include_router(company_router.router)