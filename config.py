# coding=utf8
# Debug enviroment

DEBUG = True
# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = BASE_DIR + '/templates'
STATIC_DIR = BASE_DIR + '/static'
# Define the database
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0401cy@127.0.0.1/cy_qydb'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:dbbg1015@192.168.1.106/jy_business'

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "mkoiujnbhyt"

# Secret key for signing cookies
SECRET_KEY = "+e09ZlV+DcFp4/waGQtjkqHKM/nIBJUHrV/rp85luGc="
