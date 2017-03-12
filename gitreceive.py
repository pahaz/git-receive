#!/usr/bin/env python3

# updated 2017.03.12, thanks to Pahaz Blinov

"""
Requirements:
 - apt-get install python3-pip

"""

import argparse
import logging
import cmd
import shlex
import sys

assert sys.version_info >= (3, 4), 'require python >= 3.4'

VERSION = __version__ = '0.1.1'

DESCRIPTION = """
You use `git-receive` tool v{version}
Welcome!

""".format(version=VERSION)

logger = logging.getLogger('gitshell')


# commands

def git_receive_pack(self, *args):
    "git-receive-pack"
    logger.info('git-receive-pack %r', args)

def git_upload_pack(self, *args):
    "git-upload-pack"
    logger.info('git-upload-pack %r', args)

# /commands


def setup_logging():
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    root_logger.addHandler(console)


def create_agrument_parser():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION)
    return parser


class InteractiveShell(cmd.Cmd):
    last_shell_output = ''
    use_rawinput = True
    intro = DESCRIPTION + 'Type help or ? to list commands.\n'
    prompt = '(i-shell) $ '

    def emptyline(self):
        pass

    def do_EOF(self, line):
        "exit()"
        sys.exit()

    do_q = do_quit = do_exit = do_EOF

    def do_shell(self, line):
        "Run a shell command"
        logger.info("running shell command: %s", line)
        with os.popen(line) as command:
            output = command.read()
            logger.info("command output: %r", output)
            self.last_shell_output = output

    def do_echo(self, line):
        "Print the input, replacing '$out' with the output of the last shell command"
        # Obviously not robust
        logger.info(line.replace('$out', self.last_shell_output))


def setup_cmd():
    cmd = InteractiveShell()
    commands = {
        'git-receive-pack': git_receive_pack,
        'git-upload-pack': git_upload_pack,
    }

    for name, func in commands.items():
        setattr(cmd, 'do_' + name, func)

    return cmd


def run_interactive(cmd):
    logger.info('run_interactive()')
    cmd.cmdloop()
    return 0


def run_command(cmd, args):
    logger.info('run_command() args=%r', args)
    cmd.onecmd(' '.join(args))
    return 0


def main(argv):
    setup_logging()
    parser = create_agrument_parser()
    options, remainder = parser.parse_known_args(argv)

    is_interactive_mode = not remainder
    cmd = setup_cmd()

    try:
        retcode = run_interactive(cmd) if is_interactive_mode \
            else run_command(cmd, remainder)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
        raise

    return retcode


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

