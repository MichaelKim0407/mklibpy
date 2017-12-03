import os

from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_dir, "VERSION")) as f:
    VERSION, BASE_VERSION = [line.rstrip() for line in f]

setup(
    name="mklibpy-bin",

    version=VERSION,

    packages=find_packages(),

    install_requires=[
        'mklibpy>={}'.format(BASE_VERSION)
    ],

    entry_points={
        'console_scripts': [
            'colored=mklibpy_bin.colored:main',
            'dates=mklibpy_bin.dates:main',
        ],
    },

    url="https://github.com/MichaelKim0407/mklibpy",

    license="MIT",

    author="Michael Kim",

    author_email="mkim0407@gmail.com",

    description="Command line executables for mklibpy",

    classifiers=[
        "Development Status :: 1 - Planning",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",

        "Topic :: Terminals",
        "Topic :: Utilities",
    ]
)
