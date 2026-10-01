from .theater import Theater


class VIPTheater(Theater):
    def __init__(self, number: int, seats: dict[str, int], _price: int):
        super().__init__(number, seats, _price)
