from setuptools import setup
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    sys.exit('Sorry, Python 2 < 2.7 is not supported')

if sys.version_info[0] == 3 and sys.version_info[1] < 3:
    sys.exit('Sorry, Python 3 < 3.3 is not supported')

setup(
    name="shibboleth_session_auth",

    version="0.6",

    description="Simplistic Shibboleth integration for Django sessions",
    long_description=long_description,
    url="https://github.com/esnet/shibboleth_session_auth",

    author="Jon M. Dugan",
    author_email="jdugan@es.net",

    license="BSD",

    classifiers=[
        "Development Status :: 5 - Production / Stable",

        "Intended Audience :: Developers",

        "Programming Language :: Python :: 2.7",
    ],

    keywords="Django Shibboleth",

    packages=["shibboleth_session_auth"],

    install_requires=[
    ],

)
