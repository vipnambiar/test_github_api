__author__ = 'vipin'

import json
from os import getcwd, path as pth
from subprocess import Popen, PIPE, SubprocessError
from requests.auth import HTTPBasicAuth
import requests

def _parse_token():
   '''
   :return: Application token fot Github API
   '''
   cur_dir = pth.dirname(__file__)
   token_file = pth.abspath(pth.join(cur_dir, pth.pardir, 'secret.txt'))
   with open(token_file, "r") as filehandler:
       return filehandler.read()

def _git_cmd(cmd_str, repo=getcwd()):
    try:
        proc = Popen(cmd_str, stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
    except Exception as err:
        print(err)
    else:
        if error:
            return error.decode('unicode_escape')
        else:
            return output.decode('unicode_escape')

# Unit tests
import unittest

class AuthTest(unittest.TestCase):
    @unittest.skip
    def test_parse_token(self,):
        self.assertEqual(_parse_token(), '76754b6723f3c0f309658151656bc3c1434229e9')

    @unittest.skip
    def test_connection(self,):
        user = _parse_token()
        pwd = 'x-oauth-basic'
        resp = requests.get('https://api.github.com/users/vipnambiar/repos', auth=HTTPBasicAuth(user, pwd))
        self.assertEqual(resp.status_code, 200)

        content = json.loads(resp.text)
        for item in content:
            for key, val in item.items():
                print('{0}: {1}'.format(key, val))
            print()

    def test_git_cmd(self):
        print(_git_cmd('git commit -m "removed pass cmd as string"', repo='/home/vipin/Projects/test_github_api'))
        self.assertTrue(1)
