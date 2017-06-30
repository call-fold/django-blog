#!/usr/bin/env python
# -*- coding: utf-8 -*-

from movie_crawler.common.crawler_to_html import get_links_from_html_keyword, get_links_from_html_re
from movie_crawler.common.common_movie_crawler import get_movie_download_list
from movie_crawler.common.file_common import write_result_to_txt
import os
import re


def change_code_type(input_str, encode_type):
    real_input_str = input_str.encode(encode_type)
    return real_input_str


def change_search_str(byte_input):
    temp_str = str(byte_input).replace('\\x', '%')
    return re.findall(r'b\'(.+?)\'', temp_str)[0]


def make_search_url(search_url, add_str):
    return search_url + add_str


def get_search_url(default_search_url, search_str):
    search_str_byte = change_code_type(search_str, 'gbk')
    real_search_str = change_search_str(search_str_byte)
    # 处理电影名中间的空格
    real_search_str = real_search_str.replace(' ', '%20')
    real_search_url = make_search_url(default_search_url, real_search_str)
    return real_search_url


def compile_url_movie(url):
    return 'http://www.ygdy8.com' + url


def compile_url_page(url):
    return 'http://s.dydytt.net' + url


def delete_str_last_char(str):
    str_list = list(str)
    str_list.pop()
    return "".join(str_list)


def get_all_pages(url, decode_type='utf-8'):
    page_link_list = get_links_from_html_keyword(url, '/plus/search.php?keyword=',
                                                 decode_type)
    all_real_page_link_list = []
    if page_link_list:
        last_page_link = page_link_list[len(page_link_list) - 1]
        last_page_splits = re.findall('(\S*)PageNo=(\d*)', last_page_link)
        page_link_common_body = last_page_splits[0][0] + 'PageNo='
        last_page_num = int(last_page_splits[0][1])
        all_page_link_list = []
        for i in range(last_page_num):
            page_link = page_link_common_body + str(i + 1)
            all_page_link_list.append(page_link)
        all_real_page_link_list = list(map(compile_url_page, all_page_link_list))
        return all_real_page_link_list
    else:
        all_real_page_link_list.append(url)
        return all_real_page_link_list


def get_movie_list(url, decode_type='utf-8'):
    movie_link_list = get_links_from_html_re(url, '/html/(\w*)/(\w*)/2',
                                             decode_type)
    real_movie_link_list = list(map(compile_url_movie, movie_link_list))
    return real_movie_link_list


def get_total_movie_download_list(search_index_url, decode_type='utf-8', if_add_title=False):
    page_link_list = get_all_pages(search_index_url, decode_type)
    total_movie_link_list = []
    for page_link in page_link_list:
        total_movie_link_list += get_movie_list(page_link, decode_type)
    total_movie_download_list = get_movie_download_list(total_movie_link_list,
                                                        decode_type,
                                                        if_add_title)
    return total_movie_download_list


def do_movie_search(input_name, store_dir_path):
    my_search_index_url = get_search_url('http://s.dydytt.net/plus/so.php?kwtype=0&searchtype=title&keyword=',
                                         input_name)
    search_movie_download_list = get_total_movie_download_list(my_search_index_url, 'gbk', False)
    print(input_name)
    print('num of searched movies: ' + str(len(search_movie_download_list)))
    if len(search_movie_download_list) > 0:
        write_result_to_txt(search_movie_download_list, store_dir_path,
                            input_name + '.txt')
    else:
        print('can not find links of %s' % input_name)
    print()


def main():
    input_name = input('movie to search: ')
    my_search_index_url = get_search_url('http://s.dydytt.net/plus/so.php?kwtype=0&searchtype=title&keyword=',
                                         input_name)
    search_movie_download_list = get_total_movie_download_list(my_search_index_url, 'gbk', False)
    print('num of searched movies: ' + str(len(search_movie_download_list)))
    write_result_to_txt(search_movie_download_list, os.path.abspath('.') + '/search_movies',
                        input_name + '.txt')


if __name__ == '__main__':
    main()
