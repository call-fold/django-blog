#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob


def get_file_path_list(source_path):
    target_list = []
    for file in glob.glob(source_path + '/*'):
        file_path = os.path.abspath(file)
        target_list.append(file_path)
    return target_list


def get_file_path_list_by_kind(source_path, kind_of_file):
    target_list = []
    for file in glob.glob(source_path + '/*.' + kind_of_file):
        file_path = os.path.abspath(file)
        target_list.append(file_path)
    return target_list


def get_file_name_list(source_path):
    target_list = []
    for file in glob.glob(source_path + '/*'):
        file_path, file_name = os.path.split(file)
        target_list.append(file_name)
    return target_list


def get_file_name_list_by_kind(source_path, kind_of_file):
    target_list = []
    for file in glob.glob(source_path + '/*.' + kind_of_file):
        file_path, file_name = os.path.split(file)
        target_list.append(file_name)
    return target_list


def check_folder(target_path, target_dir):
    target_dir_path = target_path + '/' + target_dir
    if not os.path.isdir(target_dir_path):
        os.mkdir(target_dir_path)
    return target_dir_path


if __name__ == '__main__':
    print(get_file_path_list('../'))
    print(get_file_path_list_by_kind('../', 'md'))
    print(get_file_name_list('../'))
    print(get_file_name_list_by_kind('../', 'md'))
    check_folder(os.path.abspath('.'), 'test')
