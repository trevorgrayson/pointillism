from os import environ, path, getcwd

DOMAIN = environ.get('domain', 'pointillism.necessaryeval.com')
HOST = environ['HOST']
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd() 

if not STATIC_DIR or STATIC_DIR == '/':
    STATIC_DIR = '/srv/vhosts/pointillism'
else:
    STATIC_DIR += '/public'


PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID', 'AaJ4Lpt2noqfdOA69GdoF-yRUlCn0rD-JK0TbOQ6fg9C4kU53K03mrvwB4Z45EhAFRUtZtDXY3nHySmX')
