from fastapi import FastAPI

from src.presentation.v1.routers import user_router
from .container import Container


container = Container()
app = FastAPI()
app.container = container
# container.wire(
#
# )


app.include_router(user_router.router)