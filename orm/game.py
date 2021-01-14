from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from orm.base import Base


class DbGame(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="games")
    game_secret = Column(String)
    try_count = Column(Integer)
    is_active = Column(Boolean)
    is_won = Column(Boolean)

    def __init__(self, user, game_secret, try_count=0, is_active=True, is_won=False):
        self.user = user
        self.game_secret = game_secret
        self.try_count = try_count
        self.is_active = is_active
        self.is_won = is_won
