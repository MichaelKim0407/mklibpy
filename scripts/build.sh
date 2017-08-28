#!/bin/bash

cwd=$(pwd)

cd $(dirname $0)

source "packaging.rc"

cd ..

package_version=$(cat "mklibpy/__init__.py" | ggrep -oP "(?<=__version__ = \")([0-9\.]*)")

if [ "${version}" != "${package_version}" ]; then
    echo "VERSION and __version__ does not match"
    exit 1
fi;

if [ -f ${dist} ]; then
    echo "Package already exists. Did you forget to increase version number?"
    exit 1
fi;

python3 setup.py sdist

cd ${cwd}
