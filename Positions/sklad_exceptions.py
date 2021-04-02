
class DataTypeError(Exception):
    """An error when TypeError data - data isn't dict"""
    def __init__(self, data, message="Ошибка формата поданных данных (не словарь)"):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'


def data_test(data):
    if type(data) != dict:
        return False
    else:
        return True


class IntTypeError(Exception):
    """An error when TypeError data - data isn't int"""
    def __init__(self, data, message="Ошибка формата поданных данных (не число)"):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'


def int_or_no(rec_str: str):
    if rec_str.isdigit():
        return int(rec_str)
    else:
        return IntTypeError


class PeriodTypeError(Exception):
    """An error when TypeError data - data isn't datetime"""
    def __init__(self, data, message="Ошибка формата поданных данных (не дата)"):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'