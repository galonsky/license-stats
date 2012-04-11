from pygithub3 import Github
from pprint import pprint
from git import *
import urllib3
import os
import shutil
import re

gh = Github()
LICENSE_PATTERN = '(LICENSE|COPYING)(\.txt)?'
REPO_PATH = './current_repo'


def getLicenseURL(user, repo, filename):
    return 'https://raw.github.com/%s/%s/master/%s' % (user, repo, filename)


def getCommitCount(repo):
    commit = repo.commit('master')
    return commit.count()


def deleteRepo():
    shutil.rmtree(REPO_PATH)


def cloneRepo(gitURL):
    return Repo.clone_from(gitURL, REPO_PATH)


def getLicense():
    license = ''
    prog = re.compile(LICENSE_PATTERN, re.IGNORECASE)
    for filename in os.listdir(REPO_PATH):
        length = len(filename)
        if not os.path.isdir(REPO_PATH + '/' + filename):
            match = prog.match(filename)
            if match and (len(match.group(0)) == length):
                f = open(REPO_PATH + '/' + filename, 'r')
                license = f.read()
                return license


def processRepo(url):

    parts = url.split('/')
    repoName = parts[-1]
    user = parts[-2]

    info = gh.repos.get(user=user, repo=repoName)
    #pprint(vars(info))
    repo = cloneRepo(info._attrs['clone_url'])

    stats = {}
    stats['license'] = getLicense()
    stats['commits'] = getCommitCount(repo)
    stats['created'] = info._attrs['created_at']
    stats['name'] = info._attrs['name']
    stats['forks'] = info._attrs['forks']
    stats['url'] = info._attrs['html_url']
    stats['git_url'] = info._attrs['git_url']
    stats['watchers'] = info._attrs['watchers']
    stats['updated'] = info._attrs['pushed_at']
    stats['language'] = info._attrs['language']
    stats['user'] = user

    pprint(stats)

    deleteRepo()
    #print getLicense(info._attrs['clone_url'])
