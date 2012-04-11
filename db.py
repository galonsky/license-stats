import pymysql
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

conn = pymysql.connect(
    host=config.get('db', 'host'), 
    port=config.getint('db', 'port'), 
    user=config.get('db', 'user'), 
    passwd=config.get('db', 'password'), 
    db=config.get('db', 'db'))