from setuptools import setup, find_packages

setup(
    name='atico',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'psycopg2',
        'sqlalchemy',
    ],
    entry_points={'scrapy': ['settings = atico.settings']}
)