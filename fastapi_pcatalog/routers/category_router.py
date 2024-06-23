from fastapi import APIRouter, status
from fastapi_pcatalog.models.category import (
    CategoryIn, Category, CategoryOut, CategoryUpdate)
from fastapi_pcatalog.repository.category import CategoryRepo


router = APIRouter()


@router.get("/", tags=["category"])
async def get_all_categories() -> list[Category]:
    categories = await CategoryRepo.get_all()
    return categories


@router.post("/", tags=["category"], status_code=status.HTTP_201_CREATED)
async def create_category(cat: CategoryIn) -> Category:
    new_category = await CategoryRepo.create(cat)
    return new_category


@router.get("/{id}", tags=["category"])
async def get_category(id: str) -> Category:
    cat = await CategoryRepo.get_one(id)
    return cat


@router.patch("/{id}", tags=["category"])
async def update_category(id: str, update_payload: CategoryUpdate) -> Category:
    cat = await CategoryRepo.update(id, update_payload)
    return cat


@router.delete("/{id}", tags=["category"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: str):
    cat = await CategoryRepo.delete(id)