#!/bin/bash

cwd=$(pwd)

cd $(dirname $0)

source "packaging.rc"

cd ..

package_version=$(cat "mklibpy/__init__.py" | ggrep -oP "(?<=__version__ = ')([^']*)")

if [[ "${version}" != "${package_version}" ]]; then
    echo "VERSION (${version}) and __version__ (${package_version}) do not match"
    exit 1
fi;

if [[ -f ${dist} ]]; then
    echo "Package with version '${version}' already exists. Did you forget to increase version number?"
    exit 1
fi;

python3 setup.py sdist

cd ${cwd}
