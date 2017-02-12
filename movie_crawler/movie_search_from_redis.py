#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import redis

strict_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=1, charset='GBK', decode_responses=True)


def get_movie_list(pattern):
    pattern = ('*' + pattern + '*').encode('gbk')
    pattern = str(pattern).replace('\\x', '%')
    pattern = re.findall(r'b\'(.+?)\'', pattern)[0]
    list_title = strict_redis.keys(pattern)
    for title in list_title:
        movie_list = strict_redis.smembers(title)
        print(title + ' :')
        for movie in movie_list:
            print(movie)


def main():
    movie_title = '海贼王'
    get_movie_list(movie_title)


if __name__ == '__main__':
    main()
