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


def choose_item(title, items):
    """목록을 번호와 함께 보여 주고, 고른 항목을 돌려준다."""
    print(f"\n--- {title} 선택 ---")
    for i in range(len(items)):
        print(f"{i + 1}. {items[i]}")
    while True:
        number = input_number("번호 입력: ")
        if 1 <= number <= len(items):
            return items[number - 1]
        print("목록에 있는 번호를 고르세요.")


def format_price(price):
    """10000 -> '10,000원' 문자열로 바꿔서 돌려준다."""
    return f"{price:,}원"


def get_menu_choice():
    """메뉴를 출력하고 고른 번호를 돌려준다."""
    print("\n===== 영화관 메뉴 =====")
    print("1. 예매하기")
    print("2. 예매 내역 보기")
    print("0. 종료")
    return input_number("메뉴 선택: ")


def make_sample_data():
    """샘플 데이터를 넣은 Cinema를 만들어 돌려준다."""
    cinema = Cinema()
    cinema.movies = ["오디세이", "일리아드"]
    cinema.customers = ["철수", "영희"]

    # 1, 3관은 일반관 / 2, 4관은 VIP관
    cinema.theaters[1] = NormalTheater(1, "오디세이", 10000)
    cinema.theaters[2] = VIPTheater(2, "오디세이", 10000)
    cinema.theaters[3] = NormalTheater(3, "일리아드", 10000)
    cinema.theaters[4] = VIPTheater(4, "일리아드", 10000)

    # 시연용으로 미리 예약된 좌석 하나
    cinema.theaters[1].reserve("주간", 2)
    cinema.reservations.append({
        "관객": "영희", "영화": "오디세이", "시간": "주간",
        "상영관": "1관", "좌석": 2, "가격": 10000,
    })
    return cinema


# ===== 클래스 =====

class Theater:
    """상영관 (부모 클래스)"""

    def __init__(self, number, movie, price):
        self.number = number
        self.movie = movie
        # 주간/야간 좌석을 따로 관리 (딕셔너리 안에 리스트)
        self.seats = {
            "주간": ["빈자리"] * 16,
            "야간": ["빈자리"] * 16,
        }
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

    def show_seats(self, time):
        print(f"\n[{time}] {self.number}관 좌석 배치도")
        for row in range(4):
            for col in range(4):
                seat = row * 4 + col + 1
                mark = "□" if self.seats[time][seat - 1] == "빈자리" else "X"
                print(f"[{seat:2} {mark}]", end=" ")
            print()

    def is_empty(self, time, seat):
        """좌석 번호가 범위 안이고 빈자리면 True"""
        if seat < 1 or seat > len(self.seats[time]):
            return False
        return self.seats[time][seat - 1] == "빈자리"

    def reserve(self, time, seat):
        """빈자리면 예약됨으로 바꾸고 True, 아니면 False"""
        if not self.is_empty(time, seat):
            return False
        self.seats[time][seat - 1] = "예약됨"
        return True

    def __str__(self):
        return f"{self.number}관 - {self.movie}"


class NormalTheater(Theater):
    """일반관: 기본 가격 그대로"""

    def __str__(self):
        return f"[일반] {self.number}관 - {self.movie} ({format_price(self.get_price())})"


class VIPTheater(Theater):
    """VIP관: 기본 가격 + 5,000원"""

    def get_price(self):                 # 부모 메서드를 다르게 동작 (오버라이딩)
        return self._price + 5000

    def __str__(self):
        return f"[VIP] {self.number}관 - {self.movie} ({format_price(self.get_price())})"


class Cinema:
    """영화관: 영화, 관객, 상영관, 예매 내역을 모두 관리"""

    def __init__(self):
        self.movies = []          # 영화 이름 리스트
        self.customers = []       # 관객 이름 리스트
        self.theaters = {}        # {관 번호: Theater 객체}
        self.reservations = []    # 예매 1건 = 딕셔너리

    def find_theater(self, movie, kind):
        """영화와 상영관 종류(일반관/VIP관)에 맞는 상영관을 찾는다."""
        for theater in self.theaters.values():
            if theater.movie == movie:
                if kind == "VIP관" and isinstance(theater, VIPTheater):
                    return theater
                if kind == "일반관" and isinstance(theater, NormalTheater):
                    return theater
        return None

    def book(self):
        """예매하기 (팀 순서도 순서대로)"""
        customer = choose_item("관객", self.customers)
        movie = choose_item("영화", self.movies)
        time = choose_item("상영시간", ["주간", "야간"])
        kind = choose_item("상영관", ["일반관", "VIP관"])

        theater = self.find_theater(movie, kind)
        if theater is None:
            print("해당 상영관이 없습니다.")
            return

        theater.show_seats(time)
        while True:
            seat = input_number("좌석 번호 입력: ")
            if theater.is_empty(time, seat):
                break
            print("이미 예약된 좌석이거나 없는 좌석입니다.")

        answer = choose_item(f"{seat}번 좌석을 예약하시겠습니까?", ["예", "아니오"])
        if answer == "아니오":
            print("예매를 취소하고 메뉴로 돌아갑니다.")
            return

        theater.reserve(time, seat)
        price = theater.get_price()
        self.reservations.append({
            "관객": customer, "영화": movie, "시간": time,
            "상영관": f"{theater.number}관", "좌석": seat, "가격": price,
        })
        print(f"\n예매 완료! {customer} / {movie} / {time} / "
              f"{theater.number}관 {seat}번 / {format_price(price)}")

    def show_reservations(self):
        if len(self.reservations) == 0:
            print("예매 내역이 없습니다.")
            return
        print("\n--- 예매 내역 ---")
        for r in self.reservations:
            print(f"{r['관객']} / {r['영화']} / {r['시간']} / "
                  f"{r['상영관']} {r['좌석']}번 / {format_price(r['가격'])}")

    def __str__(self):
        total = 0
        for r in self.reservations:
            total += r["가격"]
        return (f"영화 {len(self.movies)}편, 상영관 {len(self.theaters)}개, "
                f"예매 {len(self.reservations)}건, 총매출 {format_price(total)}")


# ===== 실행 =====

def main():
    cinema = make_sample_data()
    print("영화관 예매 프로그램을 시작합니다.")
    print(cinema)

    while True:
        choice = get_menu_choice()
        if choice == 0:
            print("\n프로그램을 종료합니다.")
            print(cinema)
            break
        elif choice == 1:
            cinema.book()
        elif choice == 2:
            cinema.show_reservations()
        else:
            print("잘못된 번호입니다.")


if __name__ == "__main__":
    main()



