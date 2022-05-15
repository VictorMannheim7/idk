import os
import urllib.parse
import motor.motor_asyncio
from utils.mongo import Document
from config import config

username = urllib.parse.quote_plus(config.MONGO_USERNAME)
password = urllib.parse.quote_plus(config.MONGO_PASSWORD)

connection_url = f"mongodb+srv://{username}:{password}@cupid.q19n6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo = motor.motor_asyncio.AsyncIOMotorClient(str(connection_url))


database=mongo["cupideconomy"]
bal= Document(database , "balance")
inv=Document(database , "inventory")
active=Document(database , "activeitems")
