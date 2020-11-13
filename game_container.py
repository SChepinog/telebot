import random


class Game:

    def __init__(self):
        self.secret_length = 4
        self.secret = ''
        self.try_count = 0
        self.is_started = False

    def start(self):
        self.secret = self.__generate_secret(self.secret_length)
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
                return 'Victory! It toke ' + str(self.try_count) + ' tries'
            else:
                result = self.__check_string(try_secret)
                self.try_count += 1
                return "Try again. It's your " + str(self.try_count) + " try\nResult: " + result

    def __check_string(self, try_secret):
        bulls = 0
        cows = 0
        for i in range(0, len(self.secret)):
            if try_secret.__contains__(self.secret[i]):
                cows += 1
            if self.secret[i] == try_secret[i]:
                bulls += 1
                cows -= 1
        return 'Bulls: ' + str(bulls) + ', Cows: ' + str(cows)

    @staticmethod
    def __generate_secret(param):
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if int(param) > 10:
            return Exception("Bad number")
        result = ''
        for i in range(0, int(param)):
            selected = random.choice(numbers)
            numbers.remove(selected)
            result += selected
        return result
