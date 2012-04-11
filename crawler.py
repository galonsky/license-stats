import redis_client
import repo
from pygithub3 import Github

gh = Github()


def crawlUsers(until):
    num = redis_client.numUsers()
    while num < until:
        seedUser = redis_client.getUser()
        for followed in gh.users.followers.list_following(seedUser).iterator():
            print 'Adding %s' % followed.login
            redis_client.addUser(followed.login)
        num = redis_client.numUsers()


def crawlRepos():
    while gh.remaining_requests == '~' or int(gh.remaining_requests) > 0:
        seedUser = redis_client.getUser()
        for watched in gh.repos.watchers.list_repos(seedUser).iterator():
            if not redis_client.repoProcessed(watched.name):
                repo.processRepo(watched)
                redis_client.addRepo(watched.name)