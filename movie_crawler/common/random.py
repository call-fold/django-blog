#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def create_random_num_list(amount, length):
    str = 'qwertyuiopasdfghjklzxcvbnm'
    b = []
    for i in range(amount):
        a = ''
        for j in range(length):
            a += random.choice(str)
        b.append(a)

    for i in range(len(b)):
        print(b[i])

    return b


def create_random_color_RGB():
    return (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))


if __name__ == '__main__':
    create_random_num_list(1, 4)
    print(create_random_color_RGB())
