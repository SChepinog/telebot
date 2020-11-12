import random


def generate_secret(param):
    if int(param) > 10 :
        return Exception("Bad number")
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    result = ''
    for i in range(0, int(param)):
        selected = random.choice(numbers)
        numbers.remove(selected)
        result += selected
    return result


class Game:

    def __init__(self):
        self.secret_length = 4
        self.secret = generate_secret(self.secret_length)

    def start(self):
        return self.secret

    def try_string(self, try_secret):
        try_secret = str(try_secret)
        if len(try_secret) != self.secret_length:
            return 'Wrong length'
        elif try_secret == self.secret:
            return 'Victory!'
        else:
            return 'Try again'
