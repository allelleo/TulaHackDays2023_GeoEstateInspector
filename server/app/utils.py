import random
import string


async def generate_password(length=10):
    return "".join(
        [random.choice(list(string.ascii_letters + string.digits)) for _ in range(length)]
    )
    
async def check_username(User, username: str)->bool:
    if await User.exists(username=username):
        return False
    return True

async def check_email(User, email: str)->bool:
    if await User.exists(email=email):
        return False
    return True
