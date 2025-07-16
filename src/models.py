import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, Enum
from sqlalchemy.orm import declarative_base, relationship 

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    books = relationship("Book", back_populates="category")

class RatingEnum(enum.Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(Numeric, nullable=False)
    availability = Column(Boolean, nullable=False)
    rating = Column(Enum(RatingEnum), nullable=False)
    image_url = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="books")

