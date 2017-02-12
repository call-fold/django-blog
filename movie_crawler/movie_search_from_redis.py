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
        list_len = strict_redis.llen(title)
        movie_list = strict_redis.lrange(title, 0, list_len)
        print(title + ' :')
        for movie in movie_list:
            print(movie)


def main():
    movie_title = '海贼王'
    get_movie_list(movie_title)


if __name__ == '__main__':
    main()
