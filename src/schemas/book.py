from pydantic import BaseModel, ConfigDict
from .category import CategoryResponse

class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    availability: bool
    rating: str
    image_url: str | None = None
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)