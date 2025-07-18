from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from ..database import Base 

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    books = relationship("Book", back_populates="category")