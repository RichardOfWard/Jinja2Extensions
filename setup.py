from setuptools import setup, find_packages
import jinja2_extensions

setup(
    name='Jinja2Extensions',
    version=jinja2_extensions.version,
    author='Richard Ward',
    author_email='richard@richard.ward.name',
    url='https://github.com/RichardOfWard/Jinja2Extensions',
    description='Tools to make writing Jinja2 extensions easier',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Jinja2',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
