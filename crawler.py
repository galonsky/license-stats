import redis_client
import repo
from pygithub3 import Github

gh = Github()


def crawlUsers(until):
    num = redis_client.numUsers()
    while num < until:
        seedUser = redis_client.getUser()
        try:
            for followed in gh.users.followers.list_following(seedUser).iterator():
                if not redis_client.userProcessed(followed.login):
                    print 'Adding %s' % followed.login
                    redis_client.addUser(followed.login)
            num = redis_client.numUsers()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            continue


def crawlRepos():
    while gh.remaining_requests == '~' or int(gh.remaining_requests) > 0:
        if redis_client.numUsers() < 100:
            crawlUsers(10000)
        seedUser = redis_client.getUser()
        redis_client.addProcessedUser(seedUser)
        print 'Seed user: %s' % seedUser
        try:
            for watched in gh.repos.watchers.list_repos(seedUser).iterator():
                if not redis_client.repoProcessed(watched.name):
                    if repo.processRepo(watched):
                        redis_client.addRepo(watched.name)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            continue
