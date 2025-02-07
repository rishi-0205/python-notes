from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    starting_bid = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    category = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


    owner = relationship("User", back_populates="listings")
    bids = relationship("Bid", back_populates="listing")
    comment = relationship("Comment", back_populates="listing")
    wishlist = relationship("Wishlist", back_populates="listing")
    wishlist = relationship("Wishlist", back_populates="listing")