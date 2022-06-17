import discord
from utils.db import *


class currency:

    @classmethod
    async def register(cls , user_id: discord.User):
        filter = {"user_id" : user_id.id}
		data = await bal.find_by_custom(filter)
		if data is None:
			data = {}
			await bal.upsert_custom(filter , data)
            await blacklist.upsert_custom(filter , data)
            await inv.upsert_custom(filter , data)
            await active.upsert_custom(filter , data)

    @classmethod
    async def add(cls , user_id: discord.User , amount: int , type:str = "wallet" or "bank"):
        filter = {"user_id" : user_id.id}
		data = await bal.find_by_custom(filter)
		data = {type: data[type] + amount}
		await bal.upsert_custom(filter , data)


    @classmethod
    async def subtract(cls , user_id: discord.User, amount: int, type: str = "wallet" or "bank"):
        filter = {"user_id" : user_id.id}
		data = await bal.find_by_custom(filter)
    	data = {type: data[type] - amount}
    	await bal.upsert_custom(filter , data)

    @classmethod
    async def get_amount(cls , user_id: discord.User, type: str = "wallet" or "bank"):
        filter = {"user_id": user_id.id}
        data = await bal.find_by_custom(filter)
        return data[type]
