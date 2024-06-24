from datetime import datetime, timezone
from fastapi import HTTPException, status
from fastapi_pcatalog.models.product import ProductIn, Product, ProductUpdate, ProductVariant
from fastapi_pcatalog.models.category import Category
from fastapi_pcatalog.models.variant import Variant, VariantBase, VariantUpdate
from beanie import WriteRules, DeleteRules



class ProductRepo:

    async def create(prod: ProductIn) -> Product:
        category = await Category.get(prod.category)
        
        if category is None:
            raise HTTPException(
                detail=f"Category id \"{prod.category}\" is not valid", 
                status_code=status.HTTP_404_NOT_FOUND
                )
        
        if not prod.variants:
            raise HTTPException(
                detail=f"Creating new Product requires including at least one variant.", 
                status_code=status.HTTP_400_BAD_REQUEST
                )
        payload_dict = prod.model_dump()
        variants = payload_dict.pop("variants")
        
        new_product = Product(**payload_dict)
        
        variants_objects = []
        for v in variants:
            variant = Variant(**v)
            variants_objects.append(variant)
        
        new_product.variants = variants_objects
        new_product.variants_count = len(variants_objects)
        new_product.total_count = sum([variant.quantity for variant in variants_objects])
        await new_product.insert(link_rule=WriteRules.WRITE)
        await new_product.sync()
        
        return new_product
    
    
    async def get_one(id: str) -> Product:
        prod = await Product.get(id, fetch_links=True)
        if prod is None:
            raise HTTPException(detail="Category doesn't exist", 
                                status_code=status.HTTP_404_NOT_FOUND)
        # await prod.fetch_link(Product.variants)
        return prod
    
    
    async def get_all() -> list[Product]:
        products = await Product.find_all().to_list()
        return products


    async def update(id: str, update_payload: ProductUpdate) -> Product:
        cat = await Product.get(id)
        if cat is None:
            raise HTTPException(detail="Category isn't valid.", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        update_data = update_payload.model_dump(exclude_unset=True)
        update_data.update(dict(
            date_modified=datetime.now(timezone.utc)
            ))
        update_query = {
            "$set": update_data
        }
        await cat.update(update_query)
        await cat.sync()
        
        return cat


    async def delete(id: str) -> dict:
        prod = await Product.get(id, fetch_links=True)
        if prod is None:
            raise HTTPException(detail="Category doesn't exist", 
                                status_code=status.HTTP_404_NOT_FOUND)
        cat_name = prod.name
        
        await prod.delete(link_rule=DeleteRules.DELETE_LINKS)
        
        return {"msg": f"Category [{cat_name}] has been deleted successfully."}


# ********************** Variants methods **********************

    async def create_variant(prod_id: str, variant_payload: VariantBase) -> Product:
        prod = await Product.get(prod_id, fetch_links=True)
        if prod is None:
            raise HTTPException(detail="Product isn't valid", 
                                status_code=status.HTTP_404_NOT_FOUND)
        new_variant = Variant(**variant_payload.model_dump())
        prod.variants.append(new_variant)
        await prod.save(link_rule=WriteRules.WRITE)
        prod.variants_count += 1
        prod.total_count += new_variant.quantity
        prod.date_modified = datetime.now(timezone.utc)
        await prod.sync()
        
        return prod


    async def get_variant(prod_id: str, var_id: str) -> ProductVariant:
        variant = await Variant.get(var_id)
        if variant is None:
            raise HTTPException(detail="Invalid variant.", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        prod = await Product.get(prod_id, fetch_links=True)
        if prod is None:
            raise HTTPException(detail="Invalid category.", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        if variant.id not in [v.id for v in prod.variants]:
            raise HTTPException(detail="Variant or Product is not valid.", 
                                status_code=status.HTTP_400_BAD_REQUEST)
        prod_dict = prod.model_dump()
        
        prod_output = ProductVariant(**prod_dict, specs=variant)
        
        return prod_output



    async def update_variant(prod_id: str, var_id: str, var_payload: VariantUpdate) -> ProductVariant:
        prod = await Product.get(prod_id, fetch_links=True)
        if prod is None:
            raise HTTPException(detail="Invalid category.", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        variant = await Variant.get(var_id)
        if variant is None:
            raise HTTPException(detail="Invalid variant.", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        if variant.id not in [vid.id for vid in prod.variants]:
            raise HTTPException(detail="Variant or Product is not valid.", 
                                status_code=status.HTTP_400_BAD_REQUEST)
        prod_vars_quantity_diff = (
            var_payload.quantity - variant.quantity
            )
        
        update_data = var_payload.model_dump(exclude_unset=True)
        update_data.update(
            {
                "date_modified": datetime.now(timezone.utc)
            }
        )
        update_query = {
            "$set": update_data
        }
        await variant.update(update_query)
        await variant.save_changes()
        prod.total_count += prod_vars_quantity_diff
        prod.date_modified = datetime.now(timezone.utc)
        await prod.save_changes()
        await prod.sync()
        
        updated_prod = await ProductRepo.get_variant(prod_id, var_id)
        
        return updated_prod


    async def delete_variant(prod_id: str, variant_id: str) -> Product:
        ...