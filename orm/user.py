from sqlalchemy import Column, String, Integer, Date, BigInteger

from orm.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    username = Column(String)
    firstname = Column(Date)
    last_name = Column(Date)

    def __init__(self, telegram_id=None, username=None, firstname=None, last_name=None):
        self.telegram_id = telegram_id
        self.username = username
        self.firstname = firstname
        self.last_name = last_name
