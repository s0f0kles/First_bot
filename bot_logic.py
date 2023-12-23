from random import choice
from random import randint
def gen_pass(pass_length):
    elements = [
        'Discord bot',
        'Python',
        'Hi!',
    ]
    password = ""

    for i in range(pass_length):
        password += choice(elements)

    return password

def gen_emodji():
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return choice(emodji)


def flip_coin():
    flip = randint(0, 2)
    if flip == 0:
        return "EAGLE"
    else:
        return "TAILS"