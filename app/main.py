from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, categories, threads, posts
from app.middlewares.process_header import ProcessHeader
from app.middlewares.auth_middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import ORIGINS

app = FastAPI(title="LoopSociety Forum API")

# Middleware setup
app.add_middleware(ProcessHeader)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

# Router setup
app.include_router(users.router, prefix="/api/v1/users", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(categories.router,
                   prefix="/api/v1/categories", tags=["Categories"])
app.include_router(threads.router, prefix="/api/v1/threads", tags=["Threads"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])
