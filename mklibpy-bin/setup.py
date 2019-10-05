from mklibpy_bin import __version__, mklibpy_requires
from setuptools import setup, find_packages

setup(
    name='mklibpy-bin',
    version=__version__,
    description='Command line executables for mklibpy',

    url='https://github.com/MichaelKim0407/mklibpy',
    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    license='MIT',

    python_requires='>=3.6',

    packages=find_packages(),

    install_requires=[
        'mklibpy>={}'.format(mklibpy_requires),
        'cached-property',
    ],

    entry_points={
        'console_scripts': [
            'colored=mklibpy_bin.colored:main',
            'dates=mklibpy_bin.dates:main',
            'ls-git=mklibpy_bin.ls_git:main',
            'pip-upgrade-all=mklibpy_bin.pip_upgrade_all:main',
            'upgrade=mklibpy_bin.upgrade_manager:main',
        ],
    },

    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Terminals',
        'Topic :: Utilities',
    ]
)
