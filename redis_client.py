import redis
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

r = redis.StrictRedis(host=config.get('redis', 'host'), port=config.getint('redis', 'port'), db=config.getint('redis', 'db'))


def addUser(user):
    return r.sadd('users', user)


def getUser():
    return r.spop('users')


def addRepo(repo):
    return r.sadd('repos', repo)


def numUsers():
    return r.scard('users')


def numRepos():
    return r.scard('repos')


def repoProcessed(repo):
    return r.sismember('repos', repo)


def userProcessed(user):
    return r.sismember('users_processed', user)


def addProcessedUser(user):
    return r.sadd('users_processed', user)
