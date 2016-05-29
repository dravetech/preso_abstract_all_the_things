# -*- coding: utf-8 -*-

import invoke
import yaml


FABRIC_FILE = "roles/fabric/vars/main.yml"


@invoke.task()
def deploy_fabric(commit=False):
    """Deploy fabric configuration."""
    commit_changes = 1 if commit else 0
    invoke.run("ansible-playbook deploy_network.yml -e commit_changes={}".format(commit_changes))


@invoke.task()
def add_link(left, right):
    """Add a link to the fabric."""
    left, left_port = left.split(":")
    right, right_port = right.split(":")

    with open(FABRIC_FILE, 'r') as f:
        content = yaml.load(f.read())

    a_link = {
        'left': left,
        'left_port': left_port,
        'right': right,
        'right_port': right_port,
    }

    found = False
    for link in content['fabric']:
        if a_link == link:
            found = True
            break
    if not found:
        content['fabric'].append(a_link)
        with open(FABRIC_FILE, 'w') as f:
            f.write(yaml.dump(content))
        print("{} added".format(a_link))
    else:
        print("{} already present".format(a_link))


@invoke.task()
def remove_link(left, right):
    """Remove a link from the fabric."""
    left, left_port = left.split(":")
    right, right_port = right.split(":")
    with open(FABRIC_FILE, 'r') as f:
        content = yaml.load(f.read())

    rm_link = {
        'left': left,
        'left_port': left_port,
        'right': right,
        'right_port': right_port,
    }

    found = False
    for index, link in enumerate(content['fabric']):
        if rm_link == link:
            found = True
            break
    if found:
        content['fabric'].pop(index)
        with open(FABRIC_FILE, 'w') as f:
            f.write(yaml.dump(content))
        print("{} removed".format(rm_link))
    else:
        print("{} wasn't found".format(rm_link))


@invoke.task()
def check_fabric_health():
    """Check fabric health."""
    invoke.run("ansible-playbook test_network.yml ")
