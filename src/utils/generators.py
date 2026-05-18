import random
import string


def random_string(length=10):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))