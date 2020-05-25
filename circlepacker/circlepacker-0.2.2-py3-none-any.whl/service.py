from fastapi import FastAPI
from circlepacker.routers import health, solves
from mangum import Mangum

app = FastAPI()

app.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    solves.router,
    prefix="/solves",
    tags=["solves"],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
async def base():
    return "Circle Packer"


handler = Mangum(app)
