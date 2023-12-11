from tortoise.fields import (
    IntField, CharField, DatetimeField
)
from tortoise.models import Model
import uuid

import bcrypt
from tortoise.fields import (
    IntField,
    CharField, ManyToManyField, OneToOneField, UUIDField, BooleanField, BinaryField, ForeignKeyField,
)
from app.utils import generate_password

class BaseModel(Model):
    """Абстрактный класс для моделей."""

    id = IntField(pk=True)

    class Meta:
        """Класс с метаданными."""

        abstract = True
        
class TimesBaseModel(BaseModel):
    """Абстрактный класс для моделей."""

    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)
    time_deleted = DatetimeField(null=True)

    class Meta:
        """Класс с метаданными."""

        abstract = True

class UserInput(TimesBaseModel):
    input_photo = CharField(max_length=200)
    output_photo = CharField(max_length=200, null=True)
    
    async def json(self):
        return {
            'input_photo': self.input_photo,
            'output_photo': self.output_photo,
            'time_created': self.time_created,
            'id': self.id
        }

class FeedBack(TimesBaseModel):
    from_user = OneToOneField('models.User', null=True)
    email = CharField(max_length=30, null=True)
    message = CharField(max_length=300)
    
    async def json(self):
        if self.from_user:
            return {
                'id': self.id,
                'user': await (await self.from_user.get()).json(),
                'message': self.message
            }
        return {
                'id': self.id,
                'email': self.email,
                'message': self.message
            }

class User(TimesBaseModel):
    """Модель базы данных для пользователя"""
    username = CharField(max_length=30, unique=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    password = BinaryField(null=True)
    email = CharField(max_length=30, unique=True)
    email_validated = BooleanField(default=False)
    uuid = UUIDField(default=uuid.uuid4, unique=True)
    is_admin = BooleanField(default=False)
    inputs = ManyToManyField('models.UserInput')
    
    async def get_history(self):
        data = []
        for item in await self.inputs.all():
            data.append(await item.json())
            
        return data
    
    async def set_password(self, password: str) -> bool:
        """Функция для изменения пароля пользователя."""
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password = password
        return True
    
    async def check_password(self, password: str) -> bool:
        """Функция для проверки пароля пользователя."""
        result = bcrypt.checkpw(password.encode("utf-8"), self.password)
        if result:
            return True
        return False
    
    async def validate_mail(self, change: bool = True) -> bool:
        """Функция валидации почты"""
        self.email_validated = True
        if change:
            self.uuid = uuid.uuid4()
        return True

    async def reset_password(self) -> str:
        """Функция востановления пароля."""
        password = await generate_password()
        await self.set_password(password)
        return password
    
    async def get_data_for_validate_email(self):
        """Функция для получения информации для подтверждения почты."""
        return self.email, self.uuid
    
    async def json(self):
        return {
            'id': self.id,
            'time_created': self.time_created,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }