"""selective.py callback plugin.

This callback only prints tasks that have been tagged with `print_action` or that have failed.

Output is a bit nicer than the default one.
"""

from __future__ import (absolute_import, division, print_function)

import difflib
import os

from ansible.plugins.callback import CallbackBase

__metaclass__ = type


COLORS = {
    'normal': '\033[0m',
    'ok': '\033[92m',
    'bold': '\033[1m',
    'not_so_bold': '\033[1m\033[34m',
    'changed': '\033[93m',
    'failed': '\033[91m',
    'endc': '\033[0m',
}


def colorize_shell(msg, color):
    """Given a string add necessary codes to format the string."""
    return '{}{}{}'.format(COLORS[color], msg, COLORS['endc'])


def dont_colorize(msg, color):
    """Given a string add necessary codes to format the string."""
    return msg


if os.environ.get('I_AM_ST2', False):
    colorize = dont_colorize
else:
    colorize = colorize_shell


class CallbackModule(CallbackBase):
    """selective.py callback plugin."""

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'selective'

    def __init__(self, display=None):
        """selective.py callback plugin."""
        super(CallbackModule, self).__init__(display)
        self.last_skipped = False
        self.last_task = None
        self.printed_last_task = False

    def _print_task(self, task_name=None):
        if task_name is None:
            task_name = self.last_task.name

        if not self.printed_last_task:
            self.printed_last_task = True
            line_length = 120
            if self.last_skipped:
                print()
            msg = colorize("# {} {}".format(task_name,
                                            '*' * (line_length - len(task_name))), 'bold')
            print(msg)

    def _indent_text(self, text, indent_level):
        lines = text.splitlines()
        result_lines = []
        for l in lines:
            result_lines.append("{}{}".format(' '*indent_level, l))
        return '\n'.join(result_lines)

    def _print_host_or_item(self, host_or_item, changed, msg, diff, is_host, error, stdout, stderr):
        if is_host:
            indent_level = 0
            name = colorize(host_or_item.name, 'not_so_bold')
        else:
            indent_level = 4
            name = colorize(unicode(host_or_item), 'bold')

        if error:
            color = 'failed'
            change_string = colorize('FAILED!!!', color)
        else:
            color = 'changed' if changed else 'ok'
            change_string = colorize("changed={}".format(changed), color)

        msg = colorize(msg, color)

        line_length = 120
        spaces = ' ' * (40-len(name)-indent_level)
        line = "{}  * {}{}- {}".format(' ' * indent_level, name, spaces, change_string)

        if len(msg) < 50:
            line += ' -- {}'.format(msg)
            print("{} {}---------".format(line, '-' * (line_length - len(line))))
        else:
            print("{} {}".format(line, '-' * (line_length - len(line))))
            print(self._indent_text(msg, indent_level+4))

        if diff is not None:
            if isinstance(diff, dict):
                diff = '\n'.join(difflib.unified_diff(diff['before'].splitlines(),
                                                      diff['after'].splitlines(),
                                                      fromfile=diff.get('before_header',
                                                                        'new_file'),
                                                      tofile=diff['after_header']))
            diff = colorize(diff, 'changed')
            print(self._indent_text(diff, indent_level+4))
        if stdout is not None:
            stdout = colorize(stdout, 'failed')
            print(self._indent_text(stdout, indent_level+4))
        if stderr is not None:
            stderr = colorize(stderr, 'failed')
            print(self._indent_text(stderr, indent_level+4))

    def v2_playbook_on_play_start(self, play):
        """Run on start of the play."""
        pass

    def v2_playbook_on_task_start(self, task, **kwargs):
        """Run when a task starts."""
        self.last_task = task
        self.printed_last_task = False

    def v2_runner_on_ok(self, result, **kwargs):
        """Run when a task finishes correctly."""
        if 'print_action' in result._task.tags or 'failed' in result._result:
            self._print_task()
            failed = 'failed' in result._result
            self.last_skipped = False
            self._print_host_or_item(result._host,
                                     result._result.get('changed', False),
                                     unicode(result._result.get('msg', '')),
                                     result._result.get('diff', None),
                                     is_host=True,
                                     error=failed,
                                     stdout=result._result.get('module_stdout', None),
                                     stderr=result._result.get('module_stderr', None),
                                     )
            if 'results' in result._result:
                for r in result._result['results']:
                    failed = 'failed' in r
                    self._print_host_or_item(r['item'],
                                             r.get('changed', False),
                                             unicode(r.get('msg', '')),
                                             r.get('diff', None),
                                             is_host=False,
                                             error=failed,
                                             stdout=r.get('module_stdout', None),
                                             stderr=r.get('module_stderr', None),
                                             )
        else:
            self.last_skipped = True
            print('.', end="")

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics."""
        print()
        self.printed_last_task = False
        self._print_task('STATS')

        for host, data in stats.processed.items():
            ok = stats.ok.get(host, 0)
            changed = stats.changed.get(host, 0)
            failed = stats.failures.get(host, 0)

            if failed:
                color = 'failed'
            elif changed:
                color = 'changed'
            else:
                color = 'ok'

            msg = '{}    : ok={}\tchanged={}\tfailed={}'.format(host, ok, changed, failed)
            print(colorize(msg, color))

    def v2_runner_on_skipped(self, result, **kwargs):
        """Run when a task is skipped."""
        pass

    v2_playbook_on_handler_task_start = v2_playbook_on_task_start
    v2_runner_on_failed = v2_runner_on_ok
    v2_runner_on_unreachable = v2_runner_on_ok
