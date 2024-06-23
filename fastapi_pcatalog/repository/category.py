from datetime import datetime, timezone
from fastapi import HTTPException, status
from fastapi_pcatalog.models.category import (
    Category, CategoryIn, CategoryOut, CategoryUpdate)
from beanie.odm.fields import PydanticObjectId


class CategoryOps:
    def __init__(self, _id: PydanticObjectId):
        self.id = _id
    
    async def get_category(self):
        cat = await Category.get(self.id)
        return cat

    async def get_parent(self):
        cat = await self.get_category()
        parent = (await Category.get(cat.parent) if cat else None)
        return parent

    async def get_children(self):
        cat = await self.get_category()
        children = ( [await Category.get(child_id) 
                    for child_id in cat.children]
                    if self.category.children 
                    else [] )
        return children

    async def get_ancestors(self):
        ancestors = []
        parent = await self.get_parent()
        while parent is not None:
            ancestors.insert(0, parent.id)
            parent = await CategoryOps(parent.id).get_parent()
        return ancestors


class CategoryRepo:

    async def create(cat: CategoryIn) -> CategoryOut:
        parent, children = None, []
        new_category = Category(**cat.model_dump())
        await new_category.insert()       
        await new_category.sync()
        
        if cat.parent:
            parent = await CategoryOps(cat.parent).get_category()
            parent.children.append(new_category.id)
            parent.date_modified = datetime.now(timezone.utc)
            await parent.save_changes()
        if cat.children:
            children = [await CategoryOps(_id).get_category() 
                        for _id in cat.children]
            for child in children:
                child.parent = new_category.id
                child.date_modified = datetime.now(timezone.utc)
                await child.save_changes()
        
        return new_category
    
    
    async def get_one(id: str) -> Category:
        cat = await Category.get(id)
        if cat is None:
            raise HTTPException(detail="Category doesn't exist", 
                                status_code=status.HTTP_404_NOT_FOUND)
        return cat
    
    
    async def get_all() -> list[Category]:
        categories = await Category.find_all().to_list()
        return categories


    async def update(id: str, update_payload: CategoryUpdate) -> Category:
        cat = await Category.get(id)
        if cat is None:
            raise HTTPException(detail="Category doesn't exist", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        update_data = update_payload.model_dump(exclude_unset=True)
        update_data.update( {"date_modified": datetime.now(timezone.utc)} )
        update_query = {
            "$set": update_data
        }
        await cat.update(update_query)
        await cat.sync()
        
        return cat


    async def delete(id: PydanticObjectId):
        cat = await Category.get(id)
        if cat is None:
            raise HTTPException(detail="Category doesn't exist", 
                                status_code=status.HTTP_404_NOT_FOUND)
        if cat.parent:
            parent = await CategoryOps(cat.parent).get_category()
            parent.children.remove(cat.id)
            await parent.save_changes()
        if cat.children:
            children = [await CategoryOps(_id).get_category() 
                        for _id in cat.children]
            for child in children:
                child.parent = cat.parent
                child.date_modified = datetime.now(timezone.utc)
                await child.save()
        await cat.delete()
        