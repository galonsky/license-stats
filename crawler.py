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
        for watched in gh.repos.watchers.list_repos(seedUser).iterator():
            if not redis_client.repoProcessed(watched.name):
                if repo.processRepo(watched):
                    redis_client.addRepo(watched.name)


def updateIssuesAndCollaborators():
    gh = Github()
    gh.users.get('galonsky')
    remaining = int(gh.remaining_requests)
    print remaining
    rows = db.getNoIssues()
    lastTime = datetime.now()
    num = 1
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
            issues = 0
            if info.has_issues:
                issues = repo.getClosedIssues(row[1], row[2]) + info.open_issues
            collabs = repo.getCollaborators(row[1], row[2])
            db.updateNoIssue(row[0], issues, collabs)
            num = remaining - int(gh.remaining_requests)
            remaining = int(gh.remaining_requests)
            print 'issues: %s' % str(issues)
            print 'collabs: %s' % str(collabs)
        except NotFound:
            continue
