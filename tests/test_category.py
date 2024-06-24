import pytest
from httpx import AsyncClient, ASGITransport
from fastapi_pcatalog.main import app
from beanie import PydanticObjectId


@pytest.mark.asyncio
async def test_category_creation(category_parent):
    child_cat_payload = {
        "name": "Laptops",
        "description": "Includes different types of Laptops for different workloads.",
        "options": ["RAM", "Display", "Storage", "Ports"],
        "parent": str(category_parent.id)
    }
    async with AsyncClient(transport=ASGITransport(app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/v1/category", json=child_cat_payload)
        assert res.status_code == 201
        assert category_parent.id == PydanticObjectId(res.json().get("parent"))
    


