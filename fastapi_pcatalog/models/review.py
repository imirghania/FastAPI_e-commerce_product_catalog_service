from datetime import datetime, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field, ConfigDict, BaseModel, EmailStr


__all__ = ("Review", )


class ReviewBase(BaseModel):
    user_id: PydanticObjectId
    user_email: EmailStr
    product_id: PydanticObjectId
    rating: float = Field(ge=1, le=5, multiple_of=0.5)
    content: str = Field(max_length=2000)


class Review(Document, ReviewBase):
    date_created: datetime = datetime.now(timezone.utc)
    date_modified: datetime = datetime.now(timezone.utc)
    
    class Settings:
        name = "reviews"
        use_state_management = True
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                        "user_id": "565r7654r87ssdhfc897",
                        "user_email": "user_email@mail.com",
                        "product_id": "565r7654r87ssdhfchs9",
                        "rating": 3.5,
                        "content": "Great Laptop, match exactly the specifications, I am satisfied with it.",
                        "date_created": datetime.now(timezone.utc),
                        "date_modified": datetime.now(timezone.utc)
                    }
        }
    )


class ReviewUpdate(ReviewBase):
    rating: Optional[float] = Field(ge=1, le=5, multiple_of=0.5)
    content: Optional[str] = Field(max_length=2000)
    date_modified: datetime = datetime.now(timezone.utc)