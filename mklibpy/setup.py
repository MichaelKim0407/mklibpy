from mklibpy import __version__
from setuptools import setup, find_packages

extra_django = [
    'django>=1.10,<2',
]
extra_django_all = [
    *extra_django,
    'django-markdownx',
]

extra_tornado = [
    'tornado==4.*',
]

extra_all = [
    *extra_django_all,
    *extra_tornado,
]

extra_test = [
    'pytest>=4',
    'pytest-cov>=2',

    'flake8',
]
extra_dev = [
    *extra_all,
    *extra_test,
]

extra_ci = [
    *extra_test,
]

setup(
    name='mklibpy',
    version=__version__,
    description='Python library created by Michael Kim',

    url='https://github.com/MichaelKim0407/mklibpy',
    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    license='MIT',

    python_requires='>=3.6',

    install_requires=[
        'cached-property',
    ],

    extras_require={
        'django': extra_django,
        'django-all': extra_django_all,

        'tornado': extra_tornado,

        'all': extra_all,

        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    packages=find_packages(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Software Development :: Libraries',
    ],
)
