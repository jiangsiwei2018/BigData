# coding=utf-8

import os
import shutil
import re
import json
import zipfile


class FileUtil:
    # file cache
    _files_cache = {'file': {}, 'len': {}}
    _file_max_lines = 10000

    @staticmethod
    def read_file(path):
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()
            return content

    @staticmethod
    def read_lines(filepath):
        with open(filepath, 'r') as fp:
            for line in fp:
                line = str(line, encoding='utf-8')
                line = line.rstrip('\r').rstrip('\n')
                if not line:
                    continue
                yield line

    @staticmethod
    def write_lines(filepath, lines):
        if filepath in FileUtil._files_cache['file']:
            FileUtil._files_cache['file'][filepath] = []
            FileUtil._files_cache['len'][filepath] = 0
        lines = lines if isinstance(lines, list) else [lines]
        for line in lines:
            FileUtil._files_cache['file'][filepath].append(line)
            FileUtil._files_cache['len'][filepath] += 1
        if FileUtil._files_cache['len'][filepath] >= FileUtil._file_max_lines:
            with open(filepath, 'a+') as fp:
                lines = FileUtil._files_cache['file'][filepath]
                fp.write('\n'.join(lines))
                fp.write('\n')
            FileUtil._files_cache['file'][filepath] = []
            FileUtil._files_cache['len'][filepath] = 0

    @staticmethod
    def flush():
        for filepath, lines in FileUtil._files_cache['file'].items():
            if lines:
                with open(filepath, 'a+') as fp:
                    fp.write('\n'.join(lines))
        FileUtil._files_cache = {'file': {}, 'len': {}}

    @staticmethod
    def read_json(filepath):
        with open(filepath, 'r', encoding='utf-8') as fp:
            return json.load(fp)

    @staticmethod
    def get_file_list(_dir, files=[], regex=''):
        if os.path.isfile(_dir):
            if regex and re.search(_dir, regex):
                files.append(_dir)
            elif not regex:
                files.append(_dir)
        elif os.path.isdir(_dir):
            for s in os.listdir(_dir):
                new_dir = os.path.join(_dir, s)
                FileUtil.get_file_list(new_dir, files)
        return files

    @staticmethod
    def get_file_name(filepath):
        return os.path.basename(filepath)

    @staticmethod
    def copy(src, dsc):
        shutil.copy(src, dsc)

    @staticmethod
    def exists(file):
        return os.path.exists(file) or file in FileUtil._files_cache['file']

    @staticmethod
    def move(src, dsc):
        shutil.move(src, dsc)

    @staticmethod
    def remove(path):
        if FileUtil.exists(path):
            os.remove(path)

    @staticmethod
    def rm_files(path):
        for file in FileUtil.get_file_list(path, []):
            FileUtil.remove(file)

    @staticmethod
    def mk_dirs(path):
        if not FileUtil.exists(path):
            os.makedirs(path)

    @staticmethod
    def rm_dir(path):
        shutil.rmtree(path, True)

    @staticmethod
    def get_file_lines(filepath):
        if FileUtil.exists(filepath):
            with open(filepath, 'r') as fp:
                return len(fp.readlines())
        return 0

    @staticmethod
    def get_abs_path(__file__, filename='patterns.json'):
        return os.path.dirname(__file__) + f'/{filename}'


class ZipFileUtil:

    @staticmethod
    def split_zipfile(zipfile_path):
        zip_path, file_path = zipfile_path.split('.zip')
        return zip_path + '.zip', file_path.lstrip('\\').lstrip('/')

    @staticmethod
    def read_file(path):
        zip_path, file_path = ZipFileUtil.split_zipfile(path)
        with zipfile.ZipFile(zip_path) as _zip:
            with _zip.open(file_path, "r") as fp:
                return str(fp.read(), encoding='utf-8')

    @staticmethod
    def read_lines(path):
        zip_path, file_path = ZipFileUtil.split_zipfile(path)
        with zipfile.ZipFile(zip_path) as _zip:
            with _zip.open(file_path, "r") as fp:
                for line in fp:
                    line = str(line, encoding='utf-8')
                    line = line.rstrip('\r').rstrip('\n')
                    if not line:
                        continue
                    yield line

    @staticmethod
    def write_file(path, _file):
        zip_path = ZipFileUtil.split_zipfile(path)[0]
        with zipfile.ZipFile(zip_path, 'w') as _zip:
            _zip.write(_file, os.path.basename(_file), zipfile.ZIP_DEFLATED)

    @staticmethod
    def write_lines(path, lines):
        zip_path, file_path = ZipFileUtil.split_zipfile(path)
        with zipfile.ZipFile(zip_path) as _zip:
            with _zip.open(file_path, "w") as fp:
                fp.write('\n'.join(lines))
                fp.write('\n')

    @staticmethod
    def flush():
        pass

    @staticmethod
    def read_json(path):
        zip_path, file_path = ZipFileUtil.split_zipfile(path)
        with zipfile.ZipFile(zip_path) as _zip:
            with _zip.open(file_path, "r") as fp:
                return json.load(fp)

    @staticmethod
    def get_file_list(zip_path, files=[], regex=''):
        f = zipfile.ZipFile(zip_path)
        for _file in f.infolist():
            if regex and re.search(regex, _file):
                files.append(_file.filename)
            elif not regex:
                files.append(_file.filename)
        return files

    @staticmethod
    def move(src, dsc):
        return shutil.move(src, dsc)

    @staticmethod
    def exists(path):
        zip_path, file_path = ZipFileUtil.split_zipfile(path)
        if file_path in ZipFileUtil.get_file_list(zip_path):
            return True
        return False

if re.search('\\.zip', __file__):
    file_util = ZipFileUtil
else:
    file_util = FileUtil

if __name__ == '__main__':
    # files = FileUtil.get_file_list(r'E:\Localcode\yidatecspider\spider_common\data', [])
    # print(files)
    # 系统文件操作
    # import os    os.path, os.walk, shutil.rmtree
    # 系统操作
    # import sys
    path1 = 'E:/LocalCode/allcode/bigdata.zip/bigdata/configure/configure.py'
    res = ZipFileUtil.read_file(path1)
    print(res)



