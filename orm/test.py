from orm.base import Base, engine, Session
from orm.game import Game
from orm.user import User

Base.metadata.create_all(engine)

session = Session()

user1 = User(telegram_id=1234, username='ahaha')
game1 = Game(user=user1, game_secret='1234', try_count=4, is_started=True)

session.add(user1)
session.add(game1)

session.commit()
session.close()
