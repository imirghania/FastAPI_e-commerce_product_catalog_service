from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_pcatalog.lib.utils import get_beanie_models


async def init_db(mongo_uri:str, db_name:str):
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    await init_beanie(database=db, 
                    document_models=get_beanie_models())
