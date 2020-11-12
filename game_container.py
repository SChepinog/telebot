import random


class Game:

    def __init__(self):
        self.secret_length = 4
        self.secret = ''
        self.try_count = 0
        self.is_started = False

    def start(self):
        self.secret = self.generate_secret(self.secret_length)
        self.try_count = 0
        self.is_started = True
        return self

    def stop(self):
        self.is_started = False

    def try_string(self, try_secret):
        if self.is_started:
            try_secret = str(try_secret)
            if len(try_secret) != self.secret_length:
                return 'Wrong length'
            elif try_secret == self.secret:
                self.try_count += 1
                self.stop()
                return 'Victory! It toke ' + str(self.try_count)
            else:
                self.try_count += 1
                return "Try again. It's your " + str(self.try_count) + " try"

    @staticmethod
    def generate_secret(param):
        if int(param) > 10:
            return Exception("Bad number")
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        result = ''
        for i in range(0, int(param)):
            selected = random.choice(numbers)
            numbers.remove(selected)
            result += selected
        return result
