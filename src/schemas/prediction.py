from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BookFeaturesResponse(BaseModel):
    category_id: int
    rating: int
    availability: bool

    model_config = ConfigDict(from_attributes=True)

class BookTrainingDataResponse(BaseModel):
    category_id: int
    rating: int
    availability: bool
    price: float 

    model_config = ConfigDict(from_attributes=True)

class PredictionCreate(BaseModel):
    book_id: int
    predicted_price: float
    model_version: str

class PredictionResponse(PredictionCreate):
    id: int
    prediction_date: datetime

    model_config = ConfigDict(from_attributes=True)

