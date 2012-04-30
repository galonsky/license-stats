import redis_client
import repo
from pygithub3 import Github
from datetime import datetime
import time
import db
from pygithub3.exceptions import NotFound

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

# legacy code for backfilling
def updateNoCollaborators():
    rows = db.getNoCollaborators()
    lastTime = datetime.now()
    num = 0
    for row in rows:
        try:
            since = (datetime.now() - lastTime).seconds
            interval = num * (3.6 / 5.0)
            if since < interval:
                wait = interval - since + 0.1
                print 'waiting %f' % wait
                time.sleep(wait)
            lastTime = datetime.now()
            print '%s/%s' % (row[1], row[2])
            info = gh.repos.get(row[1], row[2])
            num = 1
            org = info.organization.login

            collabs = repo.getOrgMembers(org)
            num = num + (collabs / 100) + 1
            db.updateNoCollab(row[0], collabs)

            print 'collabs: %s' % str(collabs)
        except NotFound:
            continue
