# 영화관 예매 프로그램
# 클래스 4개: Theater(부모), NormalTheater, VIPTheater(자식), Cinema(관리)


# ===== 클래스 밖 함수 =====


def input_number(message):
    """숫자를 입력받아 돌려준다. 숫자가 아니면 다시 입력받는다."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("숫자만 입력하세요.")


def input_name():
    """관객 이름을 입력받아 돌려준다. 빈 이름은 다시 입력받는다."""
    while True:
        name = input("관객 이름을 입력하세요: ").strip()
        if name:
            return name
        print("이름을 입력하세요.")


def choose_item(title, items):
    """목록을 번호와 함께 보여 주고, 고른 항목을 돌려준다.
    0을 고르면 None을 돌려준다 (처음 메뉴로 돌아가기)."""
    print(f"\n--- {title} 선택 ---")
    for i in range(len(items)):
        print(f"{i + 1}. {items[i]}")
    print("0. 처음 메뉴로")
    while True:
        number = input_number("번호 입력: ")
        if number == 0:
            return None
        if 1 <= number <= len(items):
            return items[number - 1]
        print("목록에 있는 번호를 고르세요.")


def format_price(price):
    """10000 -> '10,000원' 문자열로 바꿔서 돌려준다."""
    return f"{price:,}원"


def get_menu_choice(customer):
    """메뉴를 출력하고 고른 번호를 돌려준다."""
    print(f"\n===== 영화관 메뉴 (현재 관객: {customer}) =====")
    print("1. 예매하기")
    print("2. 내 예매 내역 보기")
    print("3. 관객 변경")
    print("4. 일별 매출 분석")
    print("0. 종료")
    return input_number("메뉴 선택: ")


def make_sample_data():
    """샘플 데이터를 넣은 Cinema를 만들어 돌려준다."""
    cinema = Cinema()
    cinema.movies = ["오디세이", "일리아드"]
    cinema.dates = ["10월 1일", "10월 2일", "10월 3일"]

    # 1, 3관은 일반관 / 2, 4관은 VIP관
    cinema.theaters[1] = NormalTheater(1, "오디세이", 10000)
    cinema.theaters[2] = VIPTheater(2, "오디세이", 10000)
    cinema.theaters[3] = NormalTheater(3, "일리아드", 10000)
    cinema.theaters[4] = VIPTheater(4, "일리아드", 10000)

    # 시연용으로 미리 예약된 좌석
    cinema.add_customer("영희")
    cinema.theaters[1].reserve("10월 1일", "주간", 2)
    cinema.reservations.append({
        "관객": "영희", "날짜": "10월 1일", "영화": "오디세이", "시간": "주간",
        "상영관": "1관", "좌석": 2, "가격": 10000,
    })
    return cinema


# ===== 클래스 =====


class Theater:
    """상영관 (부모 클래스)"""

    SEAT_COUNT = 4

    def __init__(self, number, movie, price):
        self.number = number
        self.movie = movie
        # 날짜+시간별로 좌석을 따로 관리: {(날짜, 시간): 좌석 리스트}
        self.seats = {}
        self._price = 0          # 밖에서 직접 바꾸지 않는 값 (캡슐화)
        self.set_price(price)

    def set_price(self, price):
        """가격은 0보다 커야 한다. 잘못된 값은 막는다."""
        if price <= 0:
            print("가격은 0보다 커야 합니다.")
            return
        self._price = price

    def get_price(self):
        return self._price

    def get_seats(self, date, time):
        """해당 날짜/시간의 좌석 리스트. 처음 찾으면 빈자리로 만든다."""
        key = (date, time)
        if key not in self.seats:
            self.seats[key] = ["빈자리"] * self.SEAT_COUNT
        return self.seats[key]

    def show_seats(self, date, time):
        seats = self.get_seats(date, time)
        print(f"\n[{date} {time}] {self.number}관 좌석 배치도")
        for i in range(len(seats)):
            print(f"{i + 1}번: {seats[i]}")

    def is_empty(self, date, time, seat):
        """좌석 번호가 범위 안이고 빈자리면 True"""
        seats = self.get_seats(date, time)
        if seat < 1 or seat > len(seats):
            return False
        return seats[seat - 1] == "빈자리"

    def reserve(self, date, time, seat):
        """빈자리면 예약됨으로 바꾸고 True, 아니면 False"""
        if not self.is_empty(date, time, seat):
            return False
        self.get_seats(date, time)[seat - 1] = "예약됨"
        return True

    def __str__(self):
        return f"{self.number}관 - {self.movie}"


class NormalTheater(Theater):
    """일반관: 기본 가격 그대로"""

    def __init__(self, number, movie, price):
        super().__init__(number, movie, price)
        # TODO:

    def __str__(self):
        return (
            f"[일반] {self.number}관 - {self.movie} ({format_price(self.get_price())})"
        )


class VIPTheater(Theater):
    """VIP관: 기본 가격 + 5,000원"""

    def __init__(self, number, movie, price):
        super().__init__(number, movie, price)
        # TODO:

    def get_price(self):  # 부모 메서드를 다르게 동작 (오버라이딩)
        return self._price + 5000

    def __str__(self):
        return (
            f"[VIP] {self.number}관 - {self.movie} ({format_price(self.get_price())})"
        )


class Cinema:
    """영화관: 영화, 관객, 상영관, 예매 내역을 모두 관리"""

    def __init__(self):
        self.movies = []          # 영화 이름 리스트
        self.dates = []           # 상영 날짜 리스트
        self.customers = []       # 관객 이름 리스트
        self.theaters = {}        # {관 번호: Theater 객체}
        self.reservations = []    # 예매 1건 = 딕셔너리

    def add_customer(self, name):
        """처음 온 관객이면 관객 목록에 추가한다."""
        if name not in self.customers:
            self.customers.append(name)

    def find_theater(self, movie, kind):
        """영화와 상영관 종류(일반관/VIP관)에 맞는 상영관을 찾는다."""
        for theater in self.theaters.values():
            if theater.movie == movie:
                if kind == "VIP관" and isinstance(theater, VIPTheater):
                    return theater
                if kind == "일반관" and isinstance(theater, NormalTheater):
                    return theater
        return None

    def choose_seat(self, theater, date, time):
        """좌석 번호를 입력받아 돌려준다. 0이면 None (처음 메뉴로)."""
        theater.show_seats(date, time)
        while True:
            seat = input_number("좌석 번호 입력 (0: 처음 메뉴로): ")
            if seat == 0:
                return None
            if theater.is_empty(date, time, seat):
                return seat
            print("이미 예약된 좌석이거나 없는 좌석입니다.")

    def book(self, customer):
        """예매하기 (팀 순서도 순서대로). 어느 단계에서든 0을 누르면 처음 메뉴로."""
        date = choose_item("날짜", self.dates)
        if date is None:
            return
        movie = choose_item("영화", self.movies)
        if movie is None:
            return
        time = choose_item("상영시간", ["주간", "야간"])
        if time is None:
            return
        kind = choose_item("상영관", ["일반관", "VIP관"])
        if kind is None:
            return

        theater = self.find_theater(movie, kind)
        if theater is None:
            print("해당 상영관이 없습니다.")
            return

        # 좌석 선택 -> 확인. '다른 좌석 선택'이면 좌석 선택부터 다시.
        while True:
            seat = self.choose_seat(theater, date, time)
            if seat is None:
                return
            answer = choose_item(f"{seat}번 좌석 예약 확인",
                                 ["예약하기", "다른 좌석 선택"])
            if answer is None:
                print("예매를 취소하고 처음 메뉴로 돌아갑니다.")
                return
            if answer == "예약하기":
                break

        theater.reserve(date, time, seat)
        price = theater.get_price()
        self.reservations.append({
            "관객": customer, "날짜": date, "영화": movie, "시간": time,
            "상영관": f"{theater.number}관", "좌석": seat, "가격": price,
        })
        print(f"\n예매 완료! {customer} / {date} / {movie} / {time} / "
              f"{theater.number}관 {seat}번 / {format_price(price)}")

    def show_reservations(self, customer):
        """해당 관객의 예매 내역만 보여 준다."""
        mine = [r for r in self.reservations if r["관객"] == customer]
        if len(mine) == 0:
            print(f"{customer}님의 예매 내역이 없습니다.")
            return
        print(f"\n--- {customer}님의 예매 내역 ---")
        total = 0
        for r in mine:
            print(f"{r['날짜']} / {r['영화']} / {r['시간']} / "
                  f"{r['상영관']} {r['좌석']}번 / {format_price(r['가격'])}")
            total += r["가격"]
        print(f"총 {len(mine)}건, {format_price(total)}")

    def show_daily_sales(self):
        """날짜별 매출 분석: 예매 건수, 관객 수, 매출, 영화별 매출"""
        if len(self.reservations) == 0:
            print("예매 내역이 없습니다.")
            return

        print("\n--- 일별 매출 분석 ---")
        grand_total = 0
        for date in self.dates:
            day = [r for r in self.reservations if r["날짜"] == date]
            if len(day) == 0:
                print(f"\n[{date}] 예매 없음")
                continue

            total = 0
            customers = []
            by_movie = {}
            for r in day:
                total += r["가격"]
                if r["관객"] not in customers:
                    customers.append(r["관객"])
                by_movie[r["영화"]] = by_movie.get(r["영화"], 0) + r["가격"]
            grand_total += total

            print(f"\n[{date}] 예매 {len(day)}건 / 관객 {len(customers)}명 / "
                  f"매출 {format_price(total)}")
            for movie, sales in by_movie.items():
                print(f"  - {movie}: {format_price(sales)}")

        print(f"\n전체 매출: {format_price(grand_total)}")

    def __str__(self):
        total = 0
        for r in self.reservations:
            total += r["가격"]
        return (f"영화 {len(self.movies)}편, 상영관 {len(self.theaters)}개, "
                f"관객 {len(self.customers)}명, "
                f"예매 {len(self.reservations)}건, 총매출 {format_price(total)}")


# ===== 실행 =====


def main():
    cinema = make_sample_data()
    print("영화관 예매 프로그램을 시작합니다.")
    print(cinema)

    customer = input_name()
    cinema.add_customer(customer)

    while True:
        choice = get_menu_choice(customer)
        if choice == 0:
            print("\n프로그램을 종료합니다.")
            print(cinema)
            break
        elif choice == 1:
            cinema.book(customer)
        elif choice == 2:
            cinema.show_reservations(customer)
        elif choice == 3:
            customer = input_name()
            cinema.add_customer(customer)
            print(f"{customer}님으로 변경되었습니다.")
        elif choice == 4:
            cinema.show_daily_sales()
        else:
            print("잘못된 번호입니다.")


if __name__ == "__main__":
    main()
