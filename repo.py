from pygithub3 import Github
from pprint import pprint
from git import Repo
import urllib3
import os
import shutil
import re

gh = Github()
LICENSE_PATTERN = '(LICENSE|COPYING)(\.txt)?'
REPO_PATH = './current_repo'


def getLicenseURL(user, repo, filename):
    return 'https://raw.github.com/%s/%s/master/%s' % (user, repo, filename)


def getLicense(gitURL):
    license = ''
    prog = re.compile(LICENSE_PATTERN, re.IGNORECASE)
    Repo.clone_from(gitURL, REPO_PATH)
    for filename in os.listdir(REPO_PATH):
        length = len(filename)
        if not os.path.isdir(REPO_PATH + '/' + filename):
            match = prog.match(filename)
            if match and (len(match.group(0)) == length):
                f = open(REPO_PATH + '/' + filename, 'r')
                license = f.read()
                break
    shutil.rmtree(REPO_PATH)
    return license


def processRepo(url):

    parts = url.split('/')
    repoName = parts[-1]
    user = parts[-2]

    info = gh.repos.get(user=user, repo=repoName)
    #pprint(vars(info))
    print getLicense(info._attrs['clone_url'])
