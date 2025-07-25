from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, func
from src.core import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    predicted_price = Column(Float, nullable=False)
    model_version = Column(String, nullable=False)
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())