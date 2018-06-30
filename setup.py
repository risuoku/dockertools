from setuptools import (
    setup,
    find_packages,
)
import importlib

_version = importlib.import_module('taiyaki').__version__
EXCLUDE_FROM_PACKAGES = []

setup (
    name='taiyaki',
    version=_version,
    author='risuoku',
    author_email='risuo.data@gmail.com',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'create_docker_mlenv = taiyaki.cmd.create_docker_mlenv:main',
        ]
    },
    install_requires=[
        'Jinja2',
    ],
)
