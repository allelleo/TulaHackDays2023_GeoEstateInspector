from app.models import User
import jwt

from app.config import SECRET

async def me_service(token: str):
    user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get('user_id')
    user = await User.get(id=user_id)
    return await user.json()

