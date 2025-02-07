from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    listings = relationship("Listing", back_populates="owner")
    bids = relationship("Bid", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    wishlist = relationship("Wishlist", back_populates="user")

    @classmethod
    def hash_password(cls, password: str):
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
