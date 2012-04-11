from pygithub3 import Github
from pprint import pprint
from git import *
import db
import os
import shutil
import re

gh = Github()
LICENSE_PATTERN = '.*(LICENSE|COPYING)(\.(txt|md))?'


def getLicenseURL(user, repo, filename):
    return 'https://raw.github.com/%s/%s/master/%s' % (user, repo, filename)


def getCommitCount(repo):
    commit = repo.head.commit
    return commit.count()


def deleteRepo(path):
    shutil.rmtree(path)


def cloneRepo(gitURL, dest):
    return Repo.clone_from(gitURL, dest)


def getLicense(path):
    license = ''
    prog = re.compile(LICENSE_PATTERN, re.IGNORECASE)
    for filename in os.listdir(path):
        if not os.path.isdir(path + '/' + filename):
            match = prog.match(filename)
            if match:
                f = open(path + '/' + filename, 'r')
                license = f.read()
                f.close()
                return license


def processRepoWithURL(url):
    parts = url.split('/')
    repoName = parts[-1]
    user = parts[-2]

    info = gh.repos.get(user=user, repo=repoName)
    return processRepo(info)


def processRepo(info):

    if not info.fork:
        return False

    print 'Processing repo: %s' % info.name
    print 'remaining requests: %s' % gh.remaining_requests
    #pprint(vars(info))
    
    parts = info.html_url.split('/')
    user = parts[-2]

    stats = {}
    stats['created'] = info.created_at
    stats['name'] = info.name
    stats['forks'] = info.forks
    stats['url'] = info.html_url
    stats['git_url'] = info.git_url
    stats['watchers'] = info.watchers
    stats['updated'] = info.pushed_at
    stats['language'] = info.language
    stats['user'] = user

    path = './current_repo/' + info.name

    try:
        repo = cloneRepo(info.clone_url, path)
        stats['commits'] = getCommitCount(repo)
        stats['license'] = getLicense(path)
        db.insertRecord(stats)
    except Exception as inst:
        print 'Caught error: \n%s' % inst
        db.insertError(stats['url'], inst.__str__())

    if os.path.exists(path):
        deleteRepo(path)

    return True
  
    #print getLicense(info._attrs['clone_url'])
