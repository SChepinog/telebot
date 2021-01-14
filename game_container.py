from tg.game import TgGame

games = {}


def _add_game(user_id):
    games[user_id] = TgGame()


def get_game_for_user(user_id):
    if not _user_has_game(user_id):
        _add_game(user_id)
    return games.get(user_id)


def _user_has_game(user_id):
    return games.keys().__contains__(user_id)
