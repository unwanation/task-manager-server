from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user, space, task

app = FastAPI(title="Overload API", root_path=f"/api/v1", version="1.0")

ORIGINS = [
    "http://localhost",
    "http://127.0.0.0",
    "http://127.0.0.0:3000",
    "http://127.0.0.0:5000",
    "http://localhost:3000",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["post", "get"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(space.router)
app.include_router(task.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
