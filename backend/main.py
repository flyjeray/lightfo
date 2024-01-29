from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth

tags_metadata = [
    {
        "name": "Auth",
        "description": "Operations that are related to User Authentication",
    },
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