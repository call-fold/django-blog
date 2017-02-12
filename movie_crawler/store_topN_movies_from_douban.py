#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
from urllib.request import urlopen


def save_list_to_redis(_table_name, name_list):
    strict_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    strict_redis.delete(_table_name)
    for code in name_list:
        strict_redis.rpush(_table_name, code)


def get_top_250_movies():
    print('begin...')
    html = r'https://api.douban.com/v2/movie/top250?start={page}'
    p = 1
    i = 1
    top_n_movie_list = []
    while p <= 13:
        try:
            url = html.format(page=(p - 1) * 20)
            response = urlopen(url)
            hjson = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(e)

        for key in hjson['subjects']:
            print(i, ': ', key['title'])
            top_n_movie_list.append(key['title'])
            i += 1
        p += 1
    return top_n_movie_list


def main():
    movie_list = get_top_250_movies()
    save_list_to_redis('top_n_movies', movie_list)


if __name__ == '__main__':
    main()
