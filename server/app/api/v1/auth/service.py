from app.schemas import SignUpModel, SignInModel
from app.models import User
from app.utils import check_email, check_username
import jwt

from app.config import SECRET


async def sign_up_service(data: SignUpModel):
    if not await check_username(User, data.username):
        raise
    if not await check_email(User, data.email):
        raise
    user = User(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email
    )
    await user.set_password(data.password)
    await user.save()
    return True

async def sign_in_service(data: SignInModel):
    user = await User.get(email=data.email)
    if await user.check_password(data.password):
        return jwt.encode({
            'user_id': user.id
        }, SECRET, algorithm='HS256')
    raise