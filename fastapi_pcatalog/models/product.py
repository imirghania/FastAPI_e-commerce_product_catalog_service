import datetime as dt
from datetime import datetime, timezone
from typing import Optional, Annotated
from beanie import Document, Link, PydanticObjectId
from pydantic import Field, ConfigDict, BaseModel, computed_field
from fastapi_pcatalog.models.brand import Brand
from fastapi_pcatalog.models.variant import Variant, VariantBase


__all__ = ("Product", )


class Description(BaseModel):
    lang: str = Field(max_length=10)
    val: str = Field(max_length=400)


class ImageSrc(BaseModel):
    src: str = Field(max_length=500)


class Image(ImageSrc):
    height: int
    width: int


class ProductBase(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[list[Description]] = Field(default_factory=list)
    brand: Optional[PydanticObjectId] = None
    category: PydanticObjectId


class ProductIn(ProductBase):
    images: Optional[list[Image]] = Field(default_factory=list)
    variants: list[VariantBase]


class Product(Document, ProductIn):
    variants: Optional[list[Link[Variant]]] = Field(default_factory=list)
    variants_count: Optional[int] = None
    total_count: Optional[int] = None
    date_created: datetime = datetime.now(timezone.utc)
    date_modified: datetime = datetime.now(timezone.utc)
    
    
    class Settings:
        name = "products"
        use_state_management = True
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                        "name": "MSI GS65 Stealth Thin 8RE",
                        "description": "Compact Gaming Laptop",
                        "images": [],
                        "brand": {
                            "name": "MSI",
                            "img": {
                                "src": "http://source-of-the-image.path"
                            }
                        },
                        "date_created": datetime.now(timezone.utc),
                        "date_modified": datetime.now(timezone.utc)
                    }
        }
    )


class ProductUpdate(Product):
    category: Optional[PydanticObjectId] = None
    variants: Optional[list[VariantBase]] = Field(default_factory=list)


class ProductVariant(ProductBase):
    specs: VariantBase


class VariantUpdate(ProductVariant):
    category: Optional[PydanticObjectId] = None