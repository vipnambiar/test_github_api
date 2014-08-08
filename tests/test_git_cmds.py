# Unit tests
import json
import requests
import unittest
from scripts.test_api import _github_get as github_get, _git_cmd as git_cmd
from scripts.test_api import _parse_token as parse_token

from github3 import login


class AuthTest(unittest.TestCase):
    @unittest.skip
    def test_parse_token(self,):
        self.assertEqual(parse_token(), '76754b6723f3c0f309658151656bc3c1434229e9')

    @unittest.skip
    def test_github_get(self,):
        url = 'https://api.github.com/repos/vipnambiar/jiva.sre.web/commits/rel_0.4'
        resp = github_get(url)
        self.assertEqual(resp.status_code, requests.codes.ok)

        content = json.loads(resp.text)
        commit_obj = content['commit']
        sha_str = content['sha']
        author_name = commit_obj['author']['name']
        author_email = commit_obj['author']['email']
        date = commit_obj['author']['date']
        message = commit_obj['message']
        print("Commit: {0}\nDate: {1}\nAuthor: {2}\nEmail: {3}\nMessage: {4}".format(sha_str,
                                                                                     date,
                                                                                     author_name,
                                                                                     author_email,
                                                                                     message))

    @unittest.skip
    def test_git_cmd(self):
        print(git_cmd(['git', 'status'], repo='/home/vipin/Projects/test_github_api'))
        self.assertTrue(1)

    #@unittest.skip
    def test_github3_api(self):
        gh = login(token=parse_token())
        repos = gh.iter_repos()
        print([repo.name for repo in repos])