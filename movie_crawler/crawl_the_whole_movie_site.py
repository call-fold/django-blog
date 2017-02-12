#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import os
import redis
from urllib import request
from lxml import etree


# 继承父类threading.Thread
class CrawlThread(threading.Thread):
    def __init__(self, url, new_dir, crawled_urls):
        threading.Thread.__init__(self)
        self.url = url
        self.new_dir = new_dir
        self.crawled_urls = crawled_urls

    # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
    def run(self):
        crawl_list_page(self.url, self.new_dir, self.crawled_urls)


start_url = "http://www.ygdy8.com/index.html"
host = "http://www.ygdy8.com"

strict_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=1, charset='GBK', decode_responses=True)


# 判断地址是否已经爬取
def is_exit(new_url, crawled_urls):
    for url in crawled_urls:
        if url == new_url:
            return True
    return False


# 获取页面资源
def get_page(url):
    try:
        f = request.urlopen(url)
        page = f.read()
    except Exception as e:
        print(e)
    else:
        return page


# 处理资源名
def change_code_type(input_str, encode_type):
    real_input_str = input_str.encode(encode_type)
    return real_input_str


def change_search_str(byte_input):
    temp_str = str(byte_input).replace('\\x', '%')
    return re.findall(r'b\'(.+?)\'', temp_str)[0]


def make_search_url(search_url, add_str):
    return search_url + add_str


def change_movie_title(default_movie_title):
    search_str_byte = change_code_type(default_movie_title, 'gbk')
    real_movie_title = change_search_str(search_str_byte)
    # 处理电影名中间的空格
    movie_title = real_movie_title.replace(' ', '%20')
    return movie_title


# 处理资源页面 爬取资源地址
def crawl_source_page(url, file_dir, file_name, crawled_urls):
    print(url)
    page = get_page(url)
    if page == "error":
        return
    crawled_urls.append(url)
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    nodes = tree.xpath("//div[@align='left']//table//a")
    try:
        # source = file_dir + "/" + filename + ".txt"
        # f = open(source, 'w')
        for node in nodes:
            source_url = node.xpath("text()")[0]
            print(source_url)
            # f.write(source_url + "\n")

            # push to redis
            strict_redis.rpush(change_movie_title(file_name), source_url)
            # strict_redis.rpush(file_name, source_url)
            # f.close()
            # if os.stat(source).st_size == 0:
            #     os.remove(source)
    except Exception as e:
        print(e)


# 解析分类文件
def crawl_list_page(index_url, file_dir, crawled_urls):
    print("正在解析分类主页资源")
    print(index_url)
    page = get_page(index_url)
    if page == "error":
        return
    crawled_urls.append(index_url)
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    nodes = tree.xpath("//div[@class='co_content8']//a")
    for node in nodes:
        url = node.xpath("@href")[0]
        if re.match(r'/', url):
            # 非分页地址 可以从中解析出视频资源地址
            if is_exit(host + url, crawled_urls):
                pass
            else:
                # 文件命名是不能出现以下特殊符号
                filename = node.xpath("text()")[0].replace("/", " ") \
                    .replace("\\", " ") \
                    .replace(":", " ") \
                    .replace("*", " ") \
                    .replace("?", " ") \
                    .replace("\"", " ") \
                    .replace("<", " ") \
                    .replace(">", " ") \
                    .replace("|", " ")
                crawl_source_page(host + url, file_dir, filename, crawled_urls)
            pass
        else:
            # 分页地址 从中嵌套再次解析
            print("分页地址 从中嵌套再次解析", url)
            index = index_url.rfind("/")
            base_url = index_url[0:index + 1]
            page_url = base_url + url
            if is_exit(page_url, crawled_urls):
                pass
            else:
                print("分页地址 从中嵌套再次解析", page_url)
                crawl_list_page(page_url, file_dir, crawled_urls)
            pass
    pass


# 解析首页
def crawl_index_page(start_url):
    print("正在爬取首页")
    page = get_page(start_url)
    if page == "error":
        return
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    nodes = tree.xpath("//div[@id='menu']//a")
    print("首页解析出地址", len(nodes), "条")
    for node in nodes:
        crawled_urls = [start_url]
        url = node.xpath("@href")[0]
        if re.match(r'/html/[A-Za-z0-9_/]+/index.html', url):
            if is_exit(host + url, crawled_urls):
                pass
            else:
                try:
                    catalog = node.xpath("text()")[0]
                    new_dir = "/home/slf/crawled_movies_redis/" + catalog
                    if os.path.exists(new_dir):
                        print('目录\"' + new_dir + '\"已存在, 不需要重新生成')
                    else:
                        os.makedirs(new_dir)
                        print("创建分类目录成功------" + new_dir)
                    thread = CrawlThread(host + url, new_dir, crawled_urls)
                    thread.start()
                except Exception as e:
                    print(e)


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
    crawl_index_page(start_url)
    # movie_title = '海贼王'
    # get_movie_list(movie_title)


if __name__ == '__main__':
    main()
