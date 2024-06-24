from datetime import datetime, timezone
from typing import Optional, Annotated
from beanie import Document, PydanticObjectId, Indexed
from pydantic import Field, ConfigDict, BaseModel


__all__ = ("Brand", )


class ImageSrc(BaseModel):
    src: str = Field(max_length=500)


class BrandBase(BaseModel):
    name: str = Field(max_length=100)
    desc: Optional[str] = Field(max_length=800)
    img: Optional[ImageSrc] = None


class Brand(Document, BrandBase):
    name: Annotated[str, Indexed(unique=True)] = Field(max_length=100)
    date_created: datetime = datetime.now(timezone.utc)
    date_modified: datetime = datetime.now(timezone.utc)
    
    class Settings:
        name = "brands"
        use_state_management = True
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                        "name": "MSI",
                        "desc": "Electronic devices Manufacturer.",
                        "img": {
                                "src": "http://source-of-the-image.path"
                            },
                        "date_created": datetime.now(timezone.utc),
                        "date_modified": datetime.now(timezone.utc)
                    }
        }
    )


class BrandOut(Brand):
    id: PydanticObjectId


class BrandUpdate(BrandBase):
    name: Optional[str] = Field(max_length=100)
    date_modified: datetime = datetime.now(timezone.utc)