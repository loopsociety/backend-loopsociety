from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, categories, threads, posts
app = FastAPI(title="LoopSociety Forum API")

app.include_router(users.router, prefix="/api/v1/users", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(categories.router,
                   prefix="/api/v1/categories", tags=["Categories"])
app.include_router(threads.router, prefix="/api/v1/threads", tags=["Threads"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])
