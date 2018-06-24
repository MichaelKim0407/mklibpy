import os

from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_dir, "VERSION")) as f:
    VERSION = f.read().rstrip()

extra_django = ['django>=1.10']
extra_tornado = ['tornado>=4']
extra_all = extra_django + extra_tornado

setup(
    name="mklibpy",

    version=VERSION,

    extras_require={
        'all': extra_all,
        'tornado': extra_tornado,
        'django': extra_django,
    },

    packages=find_packages(),

    url="https://github.com/MichaelKim0407/mklibpy",

    license="MIT",

    author="Michael Kim",

    author_email="mkim0407@gmail.com",

    description="Python library created by Michael Kim",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",

        "Topic :: Software Development :: Libraries",
    ]
)
