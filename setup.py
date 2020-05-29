#!/usr/bin/env python

import os

from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    readme = f.read()

requirements = ['requests>=2.23.0', 'twitch-python>=0.0.18', 'pytz>=2020.1', 'python-dateutil>=2.8.1']
test_requirements = ['twine>=3.1.1', 'wheel>=0.34.2']
setup_requirements = ['pipenv>=2020.5.28', 'setuptools>=47.1.1']

setup(
    author='Petter Kraabøl',
    author_email='petter.zarlach@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points=
    '''
        [console_scripts]
        tcd=tcd:main
    ''',
    description='Twitch Chat Downloader',
    install_requires=requirements,
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='Twitch',
    name='tcd',
    packages=find_packages(),
    python_requires=">=3.8",
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PetterKraabol/Twitch-Chat-Downloader',
    version='3.2.1',
    zip_safe=True,
)
