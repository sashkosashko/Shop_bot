import os
from aiogram.filters import Filter
from aiogram import Bot, types
import database.requests as rq

OWNER_ID = int(os.getenv("OWNER_ID", 0))

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        if not message.from_user:
            return False
            
        user_id = message.from_user.id
        
        if user_id == OWNER_ID:
            return True
            
        return await rq.is_user_admin(user_id)