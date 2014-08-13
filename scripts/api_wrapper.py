__author__ = 'vipin'

import base64
from functools import wraps
import json
import logging
import requests
from requests.auth import HTTPBasicAuth
import os
from os import getcwd, path as pth
from subprocess import Popen, PIPE

logging.basicConfig(level=logging.DEBUG)


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
def _github_get(url, params=None):
    """
    Queries Github API using GET protocol
    :param url: eg: https://api.github.com/users/vipnambiar
    :return: requests.response object
    """
    user = _parse_token()
    pwd = 'x-oauth-basic'
    if params:
        resp = requests.get(url, params=params, auth=HTTPBasicAuth(user, pwd))
    else:
        resp = requests.get(url, auth=HTTPBasicAuth(user, pwd))
    return resp


def _download_file(owner, repo, path, branch='master', dest_filename=None, dest=None):
    """
    Downloads specified file from the specified Github repo
    :param owner: Github user or organization
    :param repo: Github repository name
    :param path: The full path of the file to be downloaded
    :param branch: Branch name defaults to master
    :param dest_filename: Name with which the file has to be saved
    :param dest: The path were the file will be saved
    :return: filename if success else False
    """
    if not dest:
        dest = os.getcwd()
    if not dest_filename:
        dest_filename = path.rpartition('/')[-1]
    filepath = pth.join(pth.abspath(dest), dest_filename)
    filepath = pth.normpath(filepath)

    kwargs = dict()
    kwargs['api_url'] = 'https://api.github.com/repos'
    kwargs['owner'] = owner
    kwargs['repo'] = repo
    kwargs['path'] = path
    url = '{api_url}/{owner}/{repo}/contents/{path}'.format(**kwargs)
    param_dict = {'ref': branch}

    resp = _github_get(url, params=param_dict)

    logging.debug('Response status: %s', resp.status_code)
    logging.debug('Response headers: %s', resp.headers)
    logging.debug('Response text: %s', resp.text)

    if resp.status_code == requests.codes.ok:
        json_resp = json.loads(resp.text)
        encoded_content = json_resp.get('content')
        content = base64.b64decode(encoded_content)
    else:
        return False

    with open(filepath, 'wb') as fp:
        fp.write(content)

    return dest_filename


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
