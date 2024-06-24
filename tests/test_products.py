import pytest
from httpx import AsyncClient, ASGITransport
from fastapi_pcatalog.main import app
from random import randint


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@pytest.mark.asyncio
async def test_product(category_id, brand):
    data = {
        "name": "MSI G65 Stealth Thin 8RE", 
        "description": [{
            "lang": "EN",
            "val": "An elegant slim laptop, yet very powerful, equiped with high refresh rate display @144hz and sturdy light metal frame."
            }],
        "imgages": [{
            "src": "https://asset.msi.com/resize/image/global/product/product_7_20180314154529_5aa8d31965f35.png62405b38c58fe0f07fcef2367d8a9ba1/1024.png",
            "height": 819,
            "width": 1024
        }],
        "brand": str(brand.id),
        "category": str(category_id),
        "variants": [
            {
                "sku": str(random_with_N_digits(10)),
                "attributes": [
                    {
                        "name": "Display",
                        "value": 15
                    },
                    {
                        "name": "RAM",
                        "value": 16
                    },
                    {
                        "name": "Storage",
                        "value": 1024
                    },
                    {
                        "name": "Ports",
                        "value": 8
                    }
                ],
                "package_info": {
                    "dimensions": {
                        "width": 55,
                        "length": 43,
                        "height": 15
                    },
                    "weight": {
                        "val": 1.5
                    }
                },
                "usual_price": {
                    "currency": "usd",
                    "value": 1699
                },
                "discount_price": {
                    "currency": "usd",
                    "value": 1299
                },
                "quantity": 10
            }
        ]
        }
    async with AsyncClient(transport=ASGITransport(app), 
                            base_url="http://test", 
                            follow_redirects=True) as ac:
        res = await ac.post("/api/v1/product", json=data)
        assert res.status_code == 201
        assert res.json().get("variants_count") == 1
        assert res.json().get("total_count") == data["variants"][0]["quantity"]

