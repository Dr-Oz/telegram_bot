from sqlalchemy import Column, Integer, Sequence, VARCHAR

from tg_bot.infrastructures.database.modules.base import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, autoincrement=True, primary_key=True)
    category_code = Column(VARCHAR(255))
    category_name = Column(VARCHAR(255))

    subcategory_code = Column(VARCHAR(255))
    subcategory_name = Column(VARCHAR(255))

    name = Column(VARCHAR(255))
    photo = Column(VARCHAR(255))
    price = Column(Integer)

    def __repr__(self):
        return f'''
        Товар №{self.id} - {self.name}
        Цена: {self.price}
        '''
