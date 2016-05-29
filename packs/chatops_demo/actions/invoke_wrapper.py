#!/usr/bin/env python
"""Wrapper for invoke."""
from __future__ import print_function

import json
import os
import subprocess
import sys


from st2actions.runners.pythonrunner import Action


class InvokeWrapper(Action):
    """Wrapper for invoke."""

    def __init__(self, config):
        """Instantiate wrapper."""
        super(InvokeWrapper, self).__init__(config)
        self.venv_path = '/opt/stackstorm/virtualenvs/chatops_demo'
        self._set_venv()

    def _set_venv(self):
        path = '{}/bin'.format(self.venv_path)
        pythonpath = '{}/lib/python2.7/site-packages'.format(self.venv_path)
        os.environ['PATH'] = '{}:{}'.format(os.getenv('PATH'), path)
        os.environ['PYTHONPATH'] = '{}:{}'.format(os.getenv('PYTHONPATH'), pythonpath)

    def run(self, **kwargs):
        """Execute invoke."""
        cmd = ['inv']
        sudo = kwargs.pop('sudo')
        if sudo:
            cmd.insert(0, 'sudo')

        task_path = kwargs.pop('task_path')
        cmd.extend(['-r', task_path])
        cmd.append(kwargs.pop('task'))

        for k, v in kwargs.items():
            k = k.replace('_', '-')

            if isinstance(v, bool):
                if v:
                    cmd.append('--{}'.format(k))
            else:
                cmd.append('--{}={}'.format(k, v))
        os.environ['I_AM_ST2'] = '1'
        process = subprocess.Popen(cmd, cwd=task_path,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        out = out.strip()
        err = err.strip()
        print(out, file=sys.stdout, end='')
        print(err, file=sys.stderr, end='')
        return out

if __name__ == '__main__':
    invoke_wrapper = InvokeWrapper()
    invoke_wrapper.run()
