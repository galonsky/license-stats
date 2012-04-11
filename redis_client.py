import redis
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

r = redis.StrictRedis(host=config.get('redis', 'host'), port=config.getint('redis', 'port'), db=config.getint('redis', 'db'))
