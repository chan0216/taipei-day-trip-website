import mysql.connector.pooling
from decouple import config
con_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name='connection_pool',
        pool_size=10,
        host=config('host',default=''),
        database=config('database',default=''),
        user=config('user',default=''),
        password=config('password',default=''),
        )