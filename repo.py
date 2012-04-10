from pygithub3 import Github
from pprint import pprint


def processRepo(url):

    parts = url.split('/')
    repoName = parts[-1]
    user = parts[-2]

    gh = Github()
    repo = gh.repos.get(user=user, repo=repoName)
    pprint(vars(repo))
