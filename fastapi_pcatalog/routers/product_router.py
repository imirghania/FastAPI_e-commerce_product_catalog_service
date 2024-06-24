from fastapi import APIRouter, status
from fastapi_pcatalog.models.product import (
    ProductIn, Product, ProductUpdate, ProductVariant)
from fastapi_pcatalog.models.variant import VariantBase, VariantUpdate
from fastapi_pcatalog.repository.product import ProductRepo


router = APIRouter()


@router.get("/", tags=["product"])
async def get_all_products() -> list[Product]:
    categories = await ProductRepo.get_all()
    return categories


@router.post("/", tags=["product"], status_code=status.HTTP_201_CREATED)
async def create_product(cat: ProductIn) -> Product:
    new_category = await ProductRepo.create(cat)
    return new_category


@router.get("/{id}", tags=["product"])
async def get_product(id: str) -> Product:
    cat = await ProductRepo.get_one(id)
    return cat


@router.patch("/{id}", tags=["product"])
async def update_product(id: str, update_payload: ProductUpdate) -> Product:
    cat = await ProductRepo.update(id, update_payload)
    return cat


@router.delete("/{id}", tags=["product"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    await ProductRepo.delete(id)


# ********************** Variants endpoints **********************

@router.get("/{prod_id}/variant/{var_id}", tags=["variant"])
async def get_variant(prod_id: str, variant_id: str) -> ProductVariant:
    variant = await ProductRepo.get_variant(prod_id, variant_id)
    return variant


@router.post("/{id}/variant", tags=["variant"], status_code=status.HTTP_201_CREATED)
async def create_variant(id: str, variant_payload: VariantBase) -> ProductVariant:
    prod_variant = await ProductRepo.create_variant(id, variant_payload)
    return prod_variant


@router.patch("/{prod_id}/variant/{var_id}", tags=["variant"])
async def update_variant(prod_id: str, var_id: str, variant_payload: VariantUpdate) -> ProductVariant:
    prod_variant = await ProductRepo.update_variant(prod_id, var_id, variant_payload)
    return prod_variant


@router.delete("/{prod_id}/variant/{var_id}", tags=["variant"], 
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(prod_id: str, var_id: str) :
    await ProductRepo.delete_variant(prod_id, var_id)