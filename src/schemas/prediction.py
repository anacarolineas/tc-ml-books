from pydantic import BaseModel, ConfigDict


class BookFeaturesResponse(BaseModel):
    category_id: int
    rating: int
    availability: bool

    model_config = ConfigDict(from_attributes=True)