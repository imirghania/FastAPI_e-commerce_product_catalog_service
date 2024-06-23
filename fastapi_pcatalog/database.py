from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_pcatalog.core.config import settings
from fastapi_pcatalog.lib.utils import get_beanie_models


async def init_db():
    client = AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(database=client.e_commerce, 
                    document_models=get_beanie_models())
