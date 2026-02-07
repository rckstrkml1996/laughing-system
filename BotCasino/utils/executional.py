from random import randint, choice

not_random_values = [2500, 4900, 12000, 25000, 2300, 123000, 1030, 300]  # :)


def generate_last_out():
    nose = randint(0, 1)
    last_out = randint(1000, 25000)

    if nose == 1:
        last_out = choice(not_random_values)

    return last_out


def generate_online_now():
    return randint(650, 810)
