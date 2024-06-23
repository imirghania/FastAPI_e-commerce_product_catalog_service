from datetime import datetime, timezone
from fastapi import HTTPException, status
from fastapi_pcatalog.models.brand import BrandBase, Brand, BrandUpdate
from fastapi_pcatalog.models.product import Product



class BrandRepo:

    async def create(brand_in: BrandBase) -> Brand:
        ...
    
    
    async def get_one(id: str) -> Brand:
        brand = await Brand.get(id, fetch_links=True)
        if brand is None:
            raise HTTPException(detail="Brand doesn't exist", 
                                status_code=status.HTTP_404_NOT_FOUND)
        return brand
    
    
    async def get_all() -> list[Brand]:
        brands = await Brand.find_all().to_list()
        return brands


    async def update(id: str, update_payload: BrandUpdate) -> Brand:
        brand = await Brand.get(id)
        if brand is None:
            raise HTTPException(detail="Brand id isn't valid.", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        update_data = update_payload.model_dump(exclude_unset=True)
        update_data.update(dict(
            date_modified=datetime.now(timezone.utc)
            ))
        update_query = {
            "$set": update_data
        }
        await brand.update(update_query)
        await brand.sync()
        
        return brand


    async def delete(id: str) -> dict:
        brand = await Brand.get(id, fetch_links=True)
        if brand is None:
            raise HTTPException(detail="Brand id isn't valid", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        brand_products = await Product.find(brand == brand.id).to_list()
        brand_name = brand.name
        
        for prod in brand_products:
            prod.brand = None
            await prod.save_changes()
        await brand.delete()
        
        return {"msg": f"Category [{brand_name}] has been deleted successfully."}