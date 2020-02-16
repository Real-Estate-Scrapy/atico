# Atico

## Description
Scraping property details from https:/atico.es/ and store it in Postgresql database.


## Setup Environment Variables
In `settings.py` add the following configuration:
1. Database connection
    ```
    DATABASE = {
        'drivername': 'postgres',
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'username': os.environ.get('DB_USERNAME', 'user'),
        'password': os.environ.get('DB_PASSWORD', 'pwd'),
        'database': os.environ.get('DB_NAME', 'mydb')
    }
    ```
2. Database pipeline
    ```
    ITEM_PIPELINES = {
        'atico.pipelines.PostgresDBPipeline': 330
    }
    ```



## Dependencies
1. Install the following dependencies from requirements.txt
    `pip install -r requirements.txt`
    
    ```buildoutcfg
    sqlalchemy
    psycopg2
    ```

## Create eggfile
1. Create `setup.py` file at the same level as `scrapy.cfg` file with content as:
    ```
    from setuptools import setup, find_packages
    setup(
        name='atico',
        version='1.0',
        packages=find_packages(),
        install_requires=[
            'psycopg2',
            'sqlalchemy'
        ],
        entry_points={'scrapy': ['settings = atico.settings']}
    )
    ```
    
2. Execute `python setup.py bdist_egg` in folder at the same level as `scrapy.cfg` file
3. Upload the eggfile into the scrapyd server using: `curl http://localhost:6800/addversion.json -F project=atico -F version=1.0 -F egg=@dist/atico-1.0-py3.7.egg`
