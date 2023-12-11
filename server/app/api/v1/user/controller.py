from fastapi import APIRouter, Request, Depends

from app.api.v1.user.service import me_service
from app.depends import get_user
from app.models import User, UserInput, FeedBack
from app.schemas import FeedBackAuthModel, FeedBackModel
from tortoise.exceptions import DoesNotExist

user = APIRouter()

@user.post('/me')
async def me(token: str):
    return await me_service(token)

@user.post('/history')
async def my_history(user: User = Depends(get_user)):
    return await user.get_history()

@user.post('/feedback/auth')
async def feedback(data: FeedBackAuthModel):
    user = await get_user(token=data.token)
    feed = FeedBack(from_user=user, message=data.message)
    await feed.save()
    return {'status': True}

@user.post('/feedback/anonumys')
async def feedback(data: FeedBackModel):
    feed = FeedBack(email=data.email, message=data.message)
    await feed.save()
    return {'status': True}

@user.post('/feedbacks')
async def feedbacks(user: User = Depends(get_user)):
    if user.is_admin:
        data = []
        for feed in await FeedBack.all():
            data.append(await feed.json())
        return data
    raise DoesNotExist