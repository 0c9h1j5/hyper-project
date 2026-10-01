from .cinema import Cinema


def main():
    while True:
        is_quit = input("Do you want to quit? (y/n): ").strip().lower() == "y"
        if is_quit:
            break

        _ = make_sample_data()


def make_sample_data():
    sample_data = Cinema(
        movies=["Movie 1", "Movie 2"],
        customers=["철수", "영희"],
        theaters={"일반": 100, "VIP관": 150},
        reservations=[],
    )
    return sample_data


if __name__ == "__main__":
    main()
