from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, posts, users, comments

tags_metadata = [
    {
        "name": "Auth",
    },
    {
        "name": "Posts",
    },
    {
        "name": "Users",
    },
    {
        "name": "Comments",
    }
]

app = FastAPI(
    title="LightFo API",
    version="Version? The best you can find.",
    openapi_tags=tags_metadata
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(comments.router)