#!/usr/bin/env python

import os
import sys

from jinja2 import Environment, FileSystemLoader

import yaml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":

    with open(sys.argv[1], 'r') as f:
        variables = yaml.load(f.read())

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print j2_env.get_template('eos.j2').render(**variables)
