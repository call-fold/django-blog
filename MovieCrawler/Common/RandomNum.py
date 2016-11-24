#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def createNum(amount, length):
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


if __name__ == '__main__':
    createNum(1, 4)
