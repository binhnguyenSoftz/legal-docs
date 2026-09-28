import random
from datetime import date, timedelta


def add_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:  # 29/02
        return d.replace(year=d.year + years, day=28)


def between(rng: random.Random, start: date, end: date) -> date:
    return date.fromordinal(rng.randint(start.toordinal(), end.toordinal()))


def dob_for_age(rng: random.Random, age_min: int, age_max: int, as_of: date) -> date:
    """Ngày sinh để tuổi tại as_of nằm trong [age_min, age_max]."""
    earliest = add_years(as_of, -(age_max + 1)) + timedelta(days=1)
    latest = add_years(as_of, -age_min)
    return between(rng, earliest, latest)


def age_on(dob: date, on: date) -> int:
    return on.year - dob.year - ((on.month, on.day) < (dob.month, dob.day))


def parse(value: str | date) -> date:
    return value if isinstance(value, date) else date.fromisoformat(value)
