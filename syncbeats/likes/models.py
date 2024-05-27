from sqlalchemy import Column, ForeignKey, Integer
from syncbeats.database import Base
from sqlalchemy.orm import relationship

class Like(Base):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="likes")
    count = Column(Integer, default=0)