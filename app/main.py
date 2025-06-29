from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, categories, threads, posts
from app.middlewares.process_header import add_process_time_header
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import ORIGINS

app = FastAPI(title="LoopSociety Forum API")

# Middleware setup
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router setup
app.include_router(users.router, prefix="/api/v1/users", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(threads.router, prefix="/api/v1/threads", tags=["Threads"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])
