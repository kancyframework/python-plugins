#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine
#   $ pip install wheel

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# ======================================用户自定义数据开始=============================================

# 安装到本地仓库：python setup.py package
# 上传到Pypi仓库：python setup.py deploy 或者 python setup.py upload
# 上传到Pypi仓库并创建Git Tag：python setup.py publish

# 查看本地模块：pip list
# 卸载本地模块：pip uninstall xxx

# Package meta-data.
NAME = 'randomer'
VERSION = '0.0.4'
DESCRIPTION = '一个随机数操作工具类。'
URL = 'https://github.com/kancyframework/python-plugins/tree/main/randomer'
EMAIL = '793272861@qq.com'
AUTHOR = 'kancy'

# 额外单独模块
SINGLE_EXTRAS_MODULES = [
    'randomer'
]

# 强制的依赖包
REQUIRED = [
    # 'pytest-shutil'
]

# 可选的依赖包
EXTRAS = {
    # 'shutil feature': ['shutil'],
}

# 控制台脚本小工具
CONSOLE_SCRIPTS = [
    # 'kancyer=kancyer:main',
]


# ======================================用户自定义数据结束=============================================


# 获取README.md数据作为组件描述
def getReadmeDoc():
    # Note: this will only work if 'README.md' is present in your MANIFEST.in file!
    try:
        here = os.path.abspath(os.path.dirname(__file__))
        with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
            long_description = '\n' + f.read()
        return long_description
    except FileNotFoundError:
        return DESCRIPTION


# 打印日志
def boldLog(s):
    print('\033[1m{0}\033[0m'.format(s))


# 本地打包
def localPackage():
    try:
        boldLog('Removing previous builds…')
        here = os.path.abspath(os.path.dirname(__file__))
        rmtree(os.path.join(here, 'build'))
        rmtree(os.path.join(here, 'dist'))
    except OSError:
        pass
    boldLog('Building Source and Wheel (universal) distribution…')
    os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
    os.system('{0} setup.py install'.format(sys.executable))


# 部署到远程仓库
def deployPypi(confirm=False):
    if confirm:
        deploy = input("是否需要发布到Pypi仓库?（y or n）") or 'y'
    else:
        deploy = 'y'
    if deploy == 'y':
        # os.system('cls')
        boldLog('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')


# 创建Git Tag版本
def pushGitTag(confirm=False):
    if confirm:
        gitTag = input("是否需要创建Git Tag: v{0}?（y or n）".format(VERSION)) or 'y'
    else:
        gitTag = 'y'
    if gitTag == 'y':
        # os.system('cls')
        boldLog('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')


# py setup.py publish
class PublishCommand(Command):
    description = 'Build and install and deploy and push git tag the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # 本地打包
        localPackage()
        # 部署到仓库
        deployPypi(True)
        # 创建git tag
        pushGitTag(True)
        sys.exit()


# py setup.py upload
class UploadCommand(Command):
    description = 'Build and install and deploy the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # 本地打包
        localPackage()
        # 部署到仓库
        deployPypi(True)
        sys.exit()


# py setup.py package
class PackageCommand(Command):
    description = 'Build and install the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # 本地打包
        localPackage()
        sys.exit()


# 打包程序设置
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=getReadmeDoc(),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,

    # 多个复杂module，一个个写比较麻烦（导入含有__init__.py的包，排除测试包）
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # 单个简单的module打进包，单独定义
    py_modules=SINGLE_EXTRAS_MODULES,

    # python版本大于或等于3
    python_requires='>=3',

    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',

    # 如果您的软件包中包含需要安装的数据文件，请在此处指定它们。
    # 如果使用 Python 2.6 或更低版本，则这些也必须包含在 MANIFEST.in 中。
    # package_data={
    #     'data': ['data/names.dat'],
    # },

    # 尽管“package_data”是首选方法，但在某些情况下，您可能需要将数据文件放在包之外。
    # See: http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # 数据{python-home}/Lib/site-packages/组件.egg/数据文件相对路径目录
    data_files=[
        # ('数据文件相对路径目录', ['源文件文件路径']),
        ('data', ['data/names.dat'])
    ],

    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    # 执行命令 py setup.py upload ，upload方法对应的处理类是UploadCommand，入口方法是run()
    cmdclass={
        'package': PackageCommand,
        'deploy': UploadCommand,
        'upload': UploadCommand,
        'publish': PublishCommand
    },

    # 打包后会在Scripts目录生成可执行文件
    # 可执行文件名称=模块:函数
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS
    },
)
