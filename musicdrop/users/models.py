from sqlalchemy import Column, Integer, String, Date  
from musicdrop.database import Base 
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable= False)
    hashed_password = Column(String, nullable= False)

    likes = relationship("Like", back_populates="user")
    
    def __str__(self):
        return f"User {self.username}"