'''
Python CLI utility to generate new node resources for Rundeck
'''
import os
import re
import sys
import json
import logging
import urllib2
import urllib
import argparse
import platform



VAR_RUNDECK = '/var/rundeck'
def new_node(project_name, hostname, nodename, username):
    if os.path.exists(VAR_RUNDECK):
        file_path = '/var/rundeck/projects/{}/etc/resources.json'.format(
            project_name
        )
    else:
        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'resources.json')
    os_name = platform.system()
    os_version = platform.release()

    # The resources file might already have data, if so, load it here otherwise
    # carry on
    try:
        file = open(file_path)
        lines = file.read()
        if lines is not None:
            with open(file_path, 'r+') as f:
                data = json.load(f)
        else:
            data = {}
    except:
        data = {}

    data[hostname] = {}
    data[hostname]['nodename'] = nodename
    data[hostname]['hostname'] = hostname
    data[hostname]['osVersion'] = os_version
    data[hostname]['osName'] = os_name
    data[hostname]['username'] = username

    with open(file_path, 'w') as fh:
        json.dump(data, fh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rundeck Node Resources Generator')
    parser.add_argument('-p',
                        action='store',
                        dest='project',
                        help='Name of the Rundeck project')
    parser.add_argument('--host',
                        action='append',
                        dest='hosts',
                        help='Hostnames to add to resource list')
    parser.add_argument('-n',
                        action='store',
                        dest='nodename',
                        help='Name of the node to add')
    parser.add_argument('-u',
                        action='store',
                        dest='username',
                        help='User name for Rundeck to login to on the node')
    args = parser.parse_args()

    for host in args.hosts:
        if args.nodename is None:
            args.nodename = host
        new_node(args.project, host, args.nodename, args.username)
