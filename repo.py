from pygithub3 import Github
from pprint import pprint
from git import *
import db
import os
import shutil
import re
import license
import sys
import urllib, urllib2
import json
from urllib2 import HTTPError

gh = Github()
LICENSE_PATTERN = '.*(LICENSE|COPYING)(\.(txt|md))?'


def getLicenseURL(user, repo, filename):
    return 'https://raw.github.com/%s/%s/master/%s' % (user, repo, filename)


def getCommitCount(repo):
    commit = repo.head.commit
    return commit.count()


def deleteRepo(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def cloneRepo(gitURL, dest):
    return Repo.clone_from(gitURL, dest)


def getCollaborators(user, repo):
    collabs = gh.repos.collaborators.list(user, repo).all()
    return len(collabs)


def getOrgMembers(org):
    i = 1
    total = 0
    while True:
        url = 'https://api.github.com/orgs/%s/members?per_page=100&page=%d' % (urllib.quote(org), i)
        print url
        response = urllib2.urlopen(url).read()
        obj = json.loads(response)
        num = len(obj)
        total = total + num
        i = i + 1
        if num != 100:
            break
    return total


def getClosedIssues(user, repo):
    i = 1
    total = 0
    while True:
        url = 'https://api.github.com/repos/%s/%s/issues?state=closed&per_page=100&page=%d' % (urllib.quote(user), urllib.quote(repo), i)
        print url
        response = urllib2.urlopen(url).read()
        obj = json.loads(response)
        num = len(obj)
        total = total + num
        i = i + 1
        if num != 100:
            break
    return total


def getLicense(path):
    prog = re.compile(LICENSE_PATTERN, re.IGNORECASE)
    for filename in os.listdir(path):
        if not os.path.isdir(path + '/' + filename):
            match = prog.match(filename)
            if match:
                with open(path + '/' + filename, 'r') as f:
                    return f.read()


def processRepoWithURL(url):
    parts = url.split('/')
    repoName = parts[-1]
    user = parts[-2]

    info = gh.repos.get(user=user, repo=repoName)
    return processRepo(info)


def processRepo(info):

    if info.fork:
        return False

    print 'Processing repo: %s' % info.name
    print 'remaining requests: %s' % gh.remaining_requests
    
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
        print 'cloning...'
        repo = cloneRepo(info.git_url, path)
        print 'counting commits...'
        stats['commits'] = getCommitCount(repo)
        print 'getting license...'
        stats['license'] = getLicense(path)
        stats['license_type'] = None
        if not stats['license'] == None:
            print 'getting license type...'
            stats['license_type'] = license.getLicenseType(stats['license'])
        print 'getting collaborators...'
        collabs = getCollaborators(user, info.name)
        if collabs == 0:
            org = info.owner.login
            collabs = getOrgMembers(org)
        stats['collaborators'] = collabs
        stats['issues'] = 0
        if info.has_issues:
            print 'getting issues...'
            stats['issues'] = info.open_issues + getClosedIssues(user, info.name)
        print 'inserting to db...'
        db.insertRecord(stats)
        return True
    except HTTPError as http:
        if http.code == 403:
            raise
    except KeyboardInterrupt:
        print 'repo interrupt'
        sys.exit()
    except Exception as inst:
        print 'Caught error: \n%s' % inst
        if inst.__str__() == '[Errno 24] Too many open files' or inst.__str__() == 'filedescriptor out of range in select()':
            raise
        db.insertError(stats['url'], inst.__str__())
        return False
    finally:
        print 'deleting'
        deleteRepo(path)
