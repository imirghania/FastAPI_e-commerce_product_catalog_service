from datetime import datetime, timezone
from typing import Optional, Annotated
from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict


__all__ = ("Category", )


class CategoryIn(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=800)
    options: Optional[list[str]] = Field(default_factory=list)
    parent: Optional[PydanticObjectId] = Field(default=None)
    children: Optional[list[PydanticObjectId]] = Field(default_factory=list)


class Category(Document, CategoryIn):
    name: Annotated[str, Indexed(unique=True)] = Field(max_length=100)
    date_created: datetime = datetime.now(timezone.utc)
    date_modified: datetime = datetime.now(timezone.utc)
    
    class Settings:
        name = "categories"
        use_state_management = True
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                        "name": "Electronics",
                        "description": "Include sub-categories of electronic devices",
                        "parents": None,
                        "children": ["6665898c45f261bfc1f4660c",
                                    "6665898c45g261bfc1f46602",
                                    "5565898c45f261bfc1f47614"],
                        "options": [],
                        "date_created": "2024-06-09T08:01:14.732099Z",
                        "date_modified": "2024-06-09T08:01:14.732099Z"
                    }
        }
    )
    

class ParentChildId(BaseModel):
    id: PydanticObjectId


class CategoryOut(Category):
    parent: ParentChildId
    children: list[ParentChildId]


class CategoryUpdate(CategoryIn):
    name: Optional[str] = None
    date_modified: Optional[datetime] = datetime.now(timezone.utc)