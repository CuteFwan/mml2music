from setuptools import setup, find_packages
from mml2music import __version__ as version, __title__ as name, __author__ as author, __license__ as license

setup(
    name=name,
    version=version,
    author=author,
    url="https://github.com/CuteFwan/mml2music",
    license="MIT",
    description="Simple mml parser",
    keywords="mml",
    packages=find_packages()
)