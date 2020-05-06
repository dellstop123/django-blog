# from .base import *

# from .production import *

try:
    from .local import *
except:
    pass
import pymysql

pymysql.install_as_MySQLdb()
