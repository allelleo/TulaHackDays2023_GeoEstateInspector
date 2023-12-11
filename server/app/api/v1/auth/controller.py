from fastapi import APIRouter, Request

from app.schemas import SignUpModel,SignInModel
from app.api.v1.auth.service import sign_up_service, sign_in_service

auth = APIRouter()

@auth.post('/sign-up')
async def sign_up(r: Request, data: SignUpModel):
    return {'status': await sign_up_service(data)}

@auth.post('/sign-in')
async def sign_in(r: Request, data: SignInModel):
    return {'token': await sign_in_service(data)}