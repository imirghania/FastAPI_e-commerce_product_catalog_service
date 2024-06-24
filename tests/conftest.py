import pytest
import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient
from beanie import init_beanie
from fastapi_pcatalog.lib.utils import get_beanie_models
from fastapi_pcatalog.models.category import Category
from fastapi_pcatalog.models.brand import Brand
from fastapi_pcatalog.main import app



@pytest_asyncio.fixture(autouse=True)
async def init_testdb():
    db_client = AsyncMongoMockClient()
    await init_beanie(database=db_client.get_database(name="test_db"),
                            document_models=get_beanie_models())
    yield


@pytest.fixture()
def parent_category_payload():
    payload = {
        "name": "Electronics",
        "description": "Includes sub-categories of Electronics like, Phones, Laptops and PCs",
    }
    return payload


@pytest.fixture()
def child_category_payload():
    payload = {
        "name": "Laptops",
        "description": "Includes different types of Laptops for different workloads.",
        "options": ["RAM", "Display", "Storage", "Ports"],
    }
    return payload


@pytest.fixture()
def brand_payload():
    payload = {
        "name": "MSI",
        "desc": "Electronics Manufacturer",
        "img": {
            "src": "https://storage-asset.msi.com/frontend/imgs/logo.png"
        }
    }
    return payload


@pytest_asyncio.fixture()
async def category_parent(parent_category_payload):
    new_category = Category(**parent_category_payload)
    await new_category.insert()
    yield new_category


@pytest_asyncio.fixture()
async def category_child(child_category_payload, category_parent):
    child_category_payload.update({
        "parent": str(category_parent.id)
    })
    new_category = Category(**child_category_payload)
    await new_category.insert()
    yield new_category


@pytest_asyncio.fixture()
async def category_id(category_child):
    yield category_child.id


@pytest_asyncio.fixture()
async def brand(brand_payload):
    new_brand = Brand(**brand_payload)
    await new_brand.insert()
    yield new_brand