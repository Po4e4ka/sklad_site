
class DataTypeError(Exception):
    """An error when TypeError data - data isn't dict"""
    def __init__(self, data, message="Ошибка формата поданных данных (не словарь)"):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'


class PeriodTypeError(Exception):
    """An error when TypeError data - data isn't datetime"""
    def __init__(self, data, message="Ошибка формата поданных данных (не дата)"):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'