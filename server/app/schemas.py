from pydantic import BaseModel, EmailStr, Field

# ~~~~~~~~~~~~~~~ Auth Schemas ~~~~~~~~~~~~~~~ #
class SignUpModel(BaseModel):
    username: str = Field(title='username', description='user username', examples=['tula_hack_days'])
    first_name: str = Field(title='first name', description='user first name', examples=['John'])
    last_name: str = Field(title='last name', description='user last name', examples=['Doe'])
    email: EmailStr = Field(title='email', description='user email', examples=['john@example.com'])
    password: str
    
class SignInModel(BaseModel):
    email: EmailStr
    password: str
# ~~~~~~~~~~~~~~~ Auth Schemas ~~~~~~~~~~~~~~~ #

class FeedBackAuthModel(BaseModel):
    token:str
    message: str

class FeedBackModel(BaseModel):
    email: str
    message: str