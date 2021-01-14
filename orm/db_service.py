from orm.base import session_factory
from orm.game import DbGame
from orm.user import DbUser
from tg.game import TgGame
from tg.user import TgUser


def save_user(tg_user: TgUser):
    db_user = DbUser(telegram_id=tg_user.tg_id, username=tg_user.username,
                     firstname=tg_user.firstname, last_name=tg_user.last_name)
    session = session_factory()
    session.add(db_user)
    session.save()
    session.close()
    return db_user


def _get_user_if_present(tg_user: TgUser):
    session = session_factory()
    db_user = session.query(DbUser) \
        .filter(DbUser.telegram_id == tg_user.tg_id) \
        .first()
    session.close()
    return db_user


def get_user(tg_user: TgUser):
    db_user = _get_user_if_present(tg_user)
    if not db_user:
        db_user = save_user(tg_user)
    return db_user


def add_game(tg_game: TgGame, tg_user: TgUser):
    db_user = get_user(tg_user)
    db_game = DbGame(user=db_user, game_secret=tg_game.secret)
    session = session_factory()
    session.add(db_game)
    session.save()
    session.close()
    return db_game


def _get_active_game_if_present(tg_user: TgUser):
    db_user = get_user(tg_user)
    session = session_factory()
    db_game = session.query(DbGame) \
        .filter(DbGame.user == db_user) \
        .filter(DbGame.is_active is True) \
        .first()
    session.close()
    return db_game


def get_active_game(tg_user: TgUser):
    db_game = _get_active_game_if_present(tg_user)
    if not db_game:
        db_game = add_game(tg_user=tg_user, tg_game=TgGame())
    return db_game

# def get_game_for_user(tg_user: TgUser):
#     if not has_user(tg_user):
#         save_user(tg_user)
