from tg_bot.infrastructures.database.modules.base import Base
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(3000), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())