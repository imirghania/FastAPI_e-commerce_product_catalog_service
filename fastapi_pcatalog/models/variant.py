from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal, Optional, Union, TYPE_CHECKING
from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import Field, ConfigDict, BaseModel


# if TYPE_CHECKING:
#     from fastapi_pcatalog.models.product import Product


__all__ = ("Variant", )


class Attribute(BaseModel):
    name: str
    value: Union[str, int, Decimal]


class Price(BaseModel):
    currency: str
    value: float


class ImageSrc(BaseModel):
    src: str = Field(max_length=500)


class Image(ImageSrc):
    height: int
    width: int


class Dimensions(BaseModel):
    unit: Literal["cm", "ft"] = "cm"
    width: int
    length: int
    height: int


class Weight(BaseModel):
    unit: Literal["kg", "lb"] = "kg"
    val: float


class Packaging(BaseModel):
    dimensions: Dimensions
    weight: Weight


class VariantBase(Document):
    sku: str
    attributes: list[Attribute]
    package_info: Packaging
    quantity: int
    images: Optional[list[Image]] = Field(default_factory=list)
    usual_price: Price
    discount_price: Optional[Price] = None


class Variant(VariantBase):
    date_created: datetime = datetime.now(timezone.utc)
    date_modified: datetime = datetime.now(timezone.utc)
    
    class Settings:
        name = "variants"
        use_state_management = True
    
    model_config = ConfigDict(
    json_schema_extra = {
        "example": {
                    "product_id": "45467474546464",
                    "attributes": [
                        {
                        "name": 'ram',
                        "value": 32 
                        },
                        {
                        "name": 'storage type',
                        "value": 'ssd' 
                        },
                        {
                        "name": 'storage size',
                        "value": 512
                        },
                        ],
                    "usual_price": {
                        "currency": 'usd',
                        "value": 1549.99
                        },
                    "usual_price": {
                        "currency": 'usd',
                        "value": 1199.99
                        },
                    "date_created": datetime.now(timezone.utc),
                    "date_modified": datetime.now(timezone.utc)
                }
    }
)


class VariantUpdate(VariantBase):
    attributes: Optional[list[Attribute]] = None
    package_info: Optional[Packaging] = None
    quantity: Optional[int] = None
    sku: Optional[str] = None
    usual_price: Optional[Price] = None
    date_modified: Optional[datetime] = datetime.now(timezone.utc)