class Movie:
    def __init__(self, name = "odyssey", time = "day"):
        self.name = name
        self.time = time

    def show_name(self):
        print(self.name)

    def show_time(self):
        print(self.time)


class Theater:
    def __init__(self, name, type="normal"):
        self.name = name
        self.type = type

    def show_name(self):
        print(self.name)

    def room_type(self):
        print(self.type)

    def ticket(self):
        pass


class Ticket(Movie, Theater):
    """
    상영관
    좌석
    종류: 일반/VIP
    """
    pass


class Person(Movie, Theater):
    def __init__(self):
        pass


odyssey = Movie("odyssey")
iliad = Movie("iliad")
homer = Movie("homer")

odyssey.show_name()
iliad.show_name()
homer.show_name()

print("-" * 40)

t1 = Theater("상영관 1", "일반")
t2 = Theater("상영관 2", "VIP")

t1.room_type()
t2.room_type()