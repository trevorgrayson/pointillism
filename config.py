from os import environ, path, getcwd

HOST = environ['HOST']
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd() 

if not STATIC_DIR or STATIC_DIR == '/':
    STATIC_DIR = '/srv/vhosts/pointillism'
else:
    STATIC_DIR += '/public'
