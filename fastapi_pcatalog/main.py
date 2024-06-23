from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pcatalog.routers import (
    category_router, product_router, brand_router )
from fastapi_pcatalog.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=category_router.router, prefix="/category")
app.include_router(router=brand_router.router, prefix="/brand")
app.include_router(router=product_router.router, prefix="/product")