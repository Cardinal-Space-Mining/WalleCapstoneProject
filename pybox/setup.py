# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# This call to setup() does all the work
setup(
    name="pybox",
    packages=find_packages(include=['pybox']),
    version="0.1",
    description="Pygame wrapper for 8bitdo Ultimate C and XBox One controller using Xow",
    url="https://github.com/gandres42/pybox-one",
    author="Gavin Andres",
    author_email="gandres2416@gmail.com",
    license="MIT",
    install_requires=["pygame"]
)