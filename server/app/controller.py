from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

from app.db import init as init_db

init_db(app)

from app.api import auth, user, ml

app.include_router(auth, prefix='/api/v1/auth', tags=['auth', 'api', 'v1'])
app.include_router(user, prefix='/api/v1/user', tags=['user', 'api', 'v1'])
app.include_router(ml, prefix='/api/v1/ml', tags=['ml', 'api', 'v1'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")