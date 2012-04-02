from pygithub3 import Github
from pprint import pprint

gh = Github()

repo = gh.repos.get(user='copitux', repo='python-github3')

pprint(vars(repo))
