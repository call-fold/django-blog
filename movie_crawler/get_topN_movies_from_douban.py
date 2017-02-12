#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import redis

from movie_search import do_movie_search


def get_list_from_redis(_table_name):
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    list_len = r.llen(_table_name)
    return_list = r.lrange(_table_name, 0, list_len)
    return return_list


def get_top_n_movies_from_redis(n):
    get_movie_list = get_list_from_redis('top_n_movies')
    i = 1
    for name in get_movie_list:
        input_name = name.decode('utf-8')
        do_movie_search(input_name, os.path.abspath('.') + '/top_n_from_douban')
        if i >= n:
            break
        i += 1


def main():
    n = int(input('top n: '))
    get_top_n_movies_from_redis(n)


if __name__ == '__main__':
    main()
