import os
import re
from codecs import open
from distutils.core import setup

from setuptools import find_packages

_MODULE_NAME = "igm"
_PACKAGE_NAME = 'sci-igm'

here = os.path.abspath(os.path.dirname(__file__))
meta = {}
with open(os.path.join(here, _MODULE_NAME, 'config', 'meta.py'), 'r', 'utf-8') as f:
    exec(f.read(), meta)


def _load_req(file: str):
    with open(file, 'r', 'utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


requirements = _load_req('requirements.txt')

_REQ_PATTERN = re.compile('^requirements-([a-zA-Z0-9_]+)\\.txt$')
group_requirements = {
    item.group(1): _load_req(item.group(0))
    for item in [_REQ_PATTERN.fullmatch(reqpath) for reqpath in os.listdir()] if item
}

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    # information
    name=_PACKAGE_NAME,
    version=meta['__VERSION__'],
    packages=find_packages(include=(_MODULE_NAME, "%s.*" % _MODULE_NAME)),
    package_data={
        package_name: ['*.yaml', '*.yml']
        for package_name in find_packages(include=('*'))
    },
    description=meta['__DESCRIPTION__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=meta['__AUTHOR__'],
    author_email=meta['__AUTHOR_EMAIL__'],
    license='Apache License, Version 2.0',
    keywords='A simple tool for automatic parameter tuning.',
    url='https://github.com/igm4ai/igm',

    # environment
    python_requires=">=3.7",
    install_requires=requirements,
    tests_require=group_requirements['test'],
    extras_require=group_requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'igm=igm.entry:cli_entry'
        ]
    },
)
