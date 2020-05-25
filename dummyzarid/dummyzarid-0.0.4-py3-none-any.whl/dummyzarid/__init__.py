import re
from random import randrange, choice
from enum import Enum


class Gender(Enum):
    FEMALE = "4"
    MALE = "5"


class Citizenship(Enum):
    CITIZEN = "0"
    RESIDENT = "1"


def calculate_check_digit(digits):
    digits_arr = list(re.sub(r"\D", "", digits))
    num_digits = list(map(lambda d: int(d), digits_arr))

    num_digits.reverse()
    check_sum = 0
    for idx, d in enumerate(num_digits):
        if idx % 2 == 0:
            d = d * 2
            if d > 9:
                d = d - 9
        check_sum = check_sum + d

    return check_sum * 9 % 10


def generate_dummy_number(
    year="93",
    month="10",
    day="19",
    gender=Gender.MALE,
    citizenship=Citizenship.CITIZEN,
    sequence="896",
):
    values = [year, month, day, gender.value, sequence, citizenship.value, "8"]

    no_check_digit = "".join(values)
    id_number = no_check_digit + str(calculate_check_digit(no_check_digit))

    return id_number


def generate_random_dummy_number(
    year=None,
    month=None,
    day=None,
    gender=None,
    citizenship=None,
    sequence=None,
):
    if year is None:
        year = str(randrange(20, 99))
    if month is None:
        month_num = randrange(1, 12)
        month = f'{month_num:02d}'
    if day is None:
        day_num = randrange(1, 31)
        day = f'{day_num:02d}'
    if gender is None:
        gender = choice([Gender.MALE, Gender.FEMALE])
    if citizenship is None:
        citizenship = choice([Citizenship.CITIZEN, Citizenship.RESIDENT])
    if sequence is None:
        sequence_num = randrange(0, 999)
        sequence = f'{sequence_num:03d}'

    return generate_dummy_number(
        year=year,
        month=month,
        day=day,
        gender=gender,
        citizenship=citizenship,
        sequence=sequence,
    )
