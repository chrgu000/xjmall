# -*- coding: utf-8 -*-

import random

def create_token(count=32):
    random_token = "".join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba', count))
    return random_token


def create_ic(count=4):
    random_ic = "".join(
        random.sample('1234567890', count))
    return random_ic
