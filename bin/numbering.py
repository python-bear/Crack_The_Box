import random
import math


wordify = {
    ">": "larger than",
    "<": "smaller than",
    ">=": "larger than or equal to",
    "<=": "smaller than or equal to",
    "≈": "within 5% of"
}


def is_even(num):
    if (num % 2) == 0:
        return True
    return False


def is_odd(num):
    if (num % 2) == 0:
        return False
    return True


def is_prime(number: int):
    if number <= 1:
        return False
    if number <= 3:
        return True

    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True


def is_factor(number, target):
    if target == 0:
        return False
    return number % target == 0


def is_multiple(number, target):
    if number == 0:
        return False
    return target % number == 0


def find_multiples(number, low, high):
    if number == 0:
        return [0]
    elif number == 1:
        multiples = [num for num in range(low, high + 1)]
    else:
        multiples = [num for num in range(low, high + 1, number)]

    if 0 in multiples:
        return multiples[multiples.index(0) + 1:]
    else:
        return multiples


def deviate(number, delta: int = 1):
    if not isinstance(number, int):
        raise ValueError("Input must be an integer")

    min_value = number - delta
    max_value = number + delta

    if min_value < 0:
        min_value = 0

    return random.randint(min_value, max_value)


def is_perfect(number):
    if number <= 0:
        return False

    divisors_sum = sum([divisor for divisor in range(1, number) if number % divisor == 0])
    return divisors_sum == number


def is_palindromic(number):
    return str(number) == str(number)[::-1]


def is_square(number):
    if number < 0:
        return False

    sqrt = int(math.isqrt(number))
    return sqrt * sqrt == number


def is_fibonacci(number):
    if is_perfect(5 * number * number + 4) or is_perfect(5 * number * number - 4):
        return True
    else:
        return False


def is_within(target, number, deviation):
    return target in range(int(number - deviation), int(number + deviation))


def percent_of(percentage, number):
    return (percentage * number) / 100


def variation(values):
    if len(values) == 0:
        return None

    mean = sum(values)
    mean /= len(values)

    delta = 0
    for num in values:
        delta += max(mean, num) - min(mean, num)

    if sum(values) == 0:
        return 0
    else:
        return delta / sum(values) * 100
