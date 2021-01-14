from orm.base import session_factory
from orm.game import DbGame
from orm.user import DbUser

session = session_factory()

user1 = DbUser(telegram_id=1234, username='ahaha')
game1 = DbGame(user=user1, game_secret='1234', try_count=4, is_active=True)

session.add(user1)
session.add(game1)

session.commit()
session.close()
