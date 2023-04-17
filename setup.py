from setuptools import setup
import os


def read(filename):
    with open(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), filename
    ), "r") as fin:
        return fin.read()


setup(
    name='FaceBookCrawler',
    version='1.0',
    packages=['FaceBookCrawler'],
    package_dir={"": "src"},
    author='fiammahsu',
    author_email='fiamma0320@gmail.com',
    long_description=read('README.md'),
    install_requires=['colorlog', 'selenium']
)
