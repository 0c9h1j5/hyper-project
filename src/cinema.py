def input_number(message) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


class Cinema:
    def __init__(
        self,
        movies: list[str],
        customers: list[str],
        theaters: dict[str, int],
        reservations: list[dict[str, int]],
    ):
        self.movies = movies
        self.customers = customers
        self.theaters = theaters
        self.reservations = reservations

    def book(self):
        """예매하기"""
        pass

    def show_reservations(self):
        """예매 내역 출력"""

        print(self.movies)
        print(self.customers)
        print(self.theaters)
        print(self.reservations)
