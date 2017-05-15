import os

db_engine = os.getenv('DB_ENGINE')

SECRET_KEY = 'xxx'

INSTALLED_APPS = [
    'django_polyfield',
    'testapp_polyfield_basic',
] + (['testapp_polyfield_pg'] if db_engine == 'postgres' else [])

mysql_db = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'polyfield',
    'USER': 'polyfield',
    'PASSWORD': 'polyfield',
    'HOST': 'localhost',
}

postgresql_db = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'polyfield',
    'USER': 'polyfield',
    'PASSWORD': 'polyfield',
    'HOST': 'localhost',
}

sqlite_db = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
    'TEST': {'NAME': 'test_db.sqlite3'},
}

db_confs = {
    None: sqlite_db,  # default
    'mysql': mysql_db,
    'postgres': postgresql_db,
    'sqlite': sqlite_db,
}

DATABASES = {'default': db_confs[db_engine]}
