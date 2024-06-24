from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pcatalog.routers import (
    category_router, product_router, brand_router )
from fastapi_pcatalog.database import init_db
from fastapi_pcatalog.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(settings.mongo_url, settings.db_name)
    yield

app = FastAPI(docs_url="/api/docs", 
            openapi_url="/api", 
            lifespan=lifespan)

app.include_router(router=brand_router.router, prefix="/api/v1/brand")
app.include_router(router=category_router.router, prefix="/api/v1/category")
app.include_router(router=product_router.router, prefix="/api/v1/product")