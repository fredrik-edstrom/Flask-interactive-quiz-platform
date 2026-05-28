from datetime import datetime


def get_time_difference_to_now(other: datetime) -> int:
    """Returns the difference in seconds between now and another datetime object.

    Longer description...
    ...
    ...

    Args:
        other: the other datetime object to subtract now from.
    Returns:
        int: the difference in seconds.
    """

    difference = datetime.utcnow() - other
    return difference.seconds


def main():
    seconds = get_time_difference_to_now(datetime(year=2022, month=1, day=13))
    print(seconds / 60 / 60)


if __name__ == "__main__":
    main()

