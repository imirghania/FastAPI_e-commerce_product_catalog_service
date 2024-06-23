from fastapi import APIRouter, status
from fastapi_pcatalog.models.brand import BrandBase, Brand, BrandUpdate
from fastapi_pcatalog.repository.brand import BrandRepo


router = APIRouter()


@router.get("/", tags=["brand"])
async def get_all_brands() -> list[Brand]:
    categories = await BrandRepo.get_all()
    return categories


@router.post("/", tags=["brand"], status_code=status.HTTP_201_CREATED)
async def create_category(brand_in: BrandBase) -> Brand:
    new_brand = await BrandRepo.create(brand_in)
    return new_brand


@router.get("/{id}", tags=["brand"])
async def get_category(id: str) -> Brand:
    brand = await BrandRepo.get_one(id)
    return brand


@router.patch("/{id}", tags=["brand"])
async def update_category(id: str, update_payload: BrandUpdate) -> Brand:
    brand = await BrandRepo.update(id, update_payload)
    return brand


@router.delete("/{id}", tags=["brand"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: str):
    await BrandRepo.delete(id)