#!/usr/bin/env python
PACKAGE_NAME = 'cmsplugin_feed'
PACKAGE_DIR = PACKAGE_NAME
DEPENDENCIES = [
    'django-cms >=2.3.5pbs, <2.3.5pbs1000',
    'feedparser >=5.1.1',
    'BeautifulSoup >=3.2.1',
]


import os, sys

from distutils.command.install import INSTALL_SCHEMES
from setuptools import setup


def fullsplit(path, result=None):
    """
    Split a pathname into compontents (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell disutils to put the data_files in platofmr-specific installation
# locations.
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distuils doesn't have
# and easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(PACKAGE_DIR):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append(
                [dirpath, [os.path.join(dirpath, f) for f in filenames]]
                )
# Small hack for working with bdist_wininst
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

setup(
        name='cmsplugin-feed',
        version='0.2.1.pbs.10',
        description='Adds a plugin based MarkUp System for django-cms',
        author='Yann Malet, gwadeloop',
        author_email='yann.malet@gmail.com',
        url='http://bitbucket.org/yml/cmsplugin-feed',
        packages=packages,
        data_files=data_files,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
            'License :: OSI Approved :: BSD License',
            ],
        install_requires=DEPENDENCIES,
        include_package_data=True,
)
