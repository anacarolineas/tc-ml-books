from typing import Generic, List, TypeVar, Generic
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    """
    Data model for paginated results.
    """
    total_items: int = Field(..., description="Total number of items.")
    total_pages: int = Field(..., description="Total number of pages.")
    current_page: int = Field(..., description="The current page being returned.")
    page_size: int = Field(..., description="The number of items per page.")
    results: List[T] = Field(..., description="List of items in the current page.")

    model_config = ConfigDict(from_attributes=True)