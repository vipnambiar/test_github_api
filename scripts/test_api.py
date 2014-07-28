__author__ = 'vipin'

from functools import wraps
import requests
from requests.auth import HTTPBasicAuth
from os import getcwd, path as pth
from subprocess import Popen, PIPE


def log_api_rate_limit(func):
    """
    Decorator to display request rate limits info
    from response headers
    :param func: function which makes the Github API call
    :return: request.response object
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code == requests.codes.ok:
            print('Request rate limit: {0}'.format(resp.headers['X-RateLimit-Limit']))
            print('Remaining rate Limit: {0}'.format(resp.headers['X-RateLimit-Remaining']))
            print()
        return resp
    return wrapped


def _parse_token():
    """
    :return: Application token fot Github API
    """
    cur_dir = pth.dirname(__file__)
    token_file = pth.abspath(pth.join(cur_dir, pth.pardir, 'secret.txt'))
    with open(token_file, "r") as filehandler:
        return filehandler.read()


@log_api_rate_limit
def _github_get(url):
    """
    Queries Github API using GET protocol
    :param url: eg: https://api.github.com/users/vipnambiar
    :return: requests.response object
    """
    user = _parse_token()
    pwd = 'x-oauth-basic'
    return requests.get(url, auth=HTTPBasicAuth(user, pwd))


def _git_cmd(cmd_args, repo=getcwd()):
    """
    :param cmd_args: git command as a list of string. eg:- ['git' 'add' 'xyz.py', 'abc.txt']
    :param repo: The full path of the local git repository
    :return: The output or error after execution of command
    """
    try:
        proc = Popen(cmd_args, stdout=PIPE, stderr=PIPE, cwd=repo)
        output, error = proc.communicate()
    except Exception as err:
        print(err)
    else:
        if error:
            return error.decode('unicode_escape')
        else:
            return output.decode('unicode_escape')
