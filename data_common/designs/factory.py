# coding=utf-8
import inspect
import importlib
from data_common.designs.singleton import SingletonType
from data_common.utils.file_util import file_util, ZipFileUtil


class FactoryClass(metaclass=SingletonType):

    @staticmethod
    def get_module_members(module):
        if inspect.ismodule(module):
            members1 = inspect.getmembers(module)
            members2 = dict([member for member in members1
                             if member[0] != '__builtins__'])
            return members2
        return {}

    @staticmethod
    def get_module_prefix(module):
        members = FactoryClass.get_module_members(module)
        package = members.get('__package__')
        return package.split('.')[0]

    @staticmethod
    def import_module(_file, prefix):
        suffix = _file.split(prefix)[-1].strip('.py')
        suffix = suffix.replace('/', '.').replace('\\', '.')
        child_module_name = f'{prefix}{suffix}'
        return importlib.import_module(child_module_name)

    @staticmethod
    def get_module_children(module, regex=''):
        members = FactoryClass.get_module_members(module)
        package = members.get('__package__')
        prefix = package.split('.')[0]
        path = members.get('__path__')[0]
        children = []
        for _file in file_util.get_file_list(path, [], regex):
            if not _file.endswith('.py') or '__init__' in _file:
                continue
            child_module = FactoryClass.import_module(_file, prefix)
            children.append(child_module)
        return children

    @staticmethod
    def get_zipfile_module_children(zip_path):
        """获取zip文件中的所有模块名"""
        sys.path.append(zip_path)
        file_list = ZipFileUtil.get_file_list(zip_path, [])
        children = []
        for _file in file_list:
            if not _file.endswith('.py') or '__init__' in _file:
                continue
            _file = f'{zip_path}/{_file}'
            child_module = FactoryClass.import_module(_file, 'sites')
            children.append(child_module)
        sys.path.remove(zip_path)
        return children

    @staticmethod
    def check_module_attrs(_class, attrs):
        flag = True
        if not attrs:
            return flag
        for attr in attrs:
            if not hasattr(_class, attr):
                flag = False
                break
        return flag

    @staticmethod
    def get_factory_class_list(base, module, regex='', attrs=[]):
        class_list = []
        module_children = FactoryClass.get_module_children(module, regex)
        for module in module_children:
            for name, _class in FactoryClass.get_module_members(module).items():
                if inspect.isclass(_class) \
                        and issubclass(_class, base) and _class != base \
                        and FactoryClass.check_module_attrs(_class, attrs):
                    class_list.append(_class)
                elif not base and FactoryClass.check_module_attrs(_class, attrs):
                    class_list.append(_class)
        return class_list


if __name__ == '__main__':
    import re
    import os
    import sys
    from data_common import father_dir

    zip_path = f'{father_dir}/sites.zip'
    for item in FactoryClass.get_zipfile_module_children(zip_path):
        print(item)
