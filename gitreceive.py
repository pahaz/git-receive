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

VERSION = __version__ = '0.1.0'

DESCRIPTION = """
You use `git-receive` tool v{version}
Welcome!

""".format(version=VERSION)

COMMANDS = {
    
}

logger = logging.getLogger('gitshell')


# commands

def git_receive_pack():
    "git-receive-pack"

def git_upload_pack():
    "git-upload-pack"

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
    use_rawinput = True
    intro = DESCRIPTION + 'Type help or ? to list commands.\n'
    prompt = '(i-shell) $ '

    def emptyline(self):
        logger.info('Cmd.emptyline()')

    def default(self, line):
        # Tie in the default command processor to
        # dispatch commands known to the command manager.
        # We send the message through our parent app,
        # since it already has the logic for executing
        # the subcommand.
        line_parts = shlex.split(line)
        logger.info('Cmd.default() line_parts=%r', line_parts)

    def do_EOF(self, line):
        "exit()"
        sys.exit()

    do_q = do_quit = do_exit = do_EOF


def run_interactive():
    logger.info('run_interactive()')
    InteractiveShell().cmdloop()


def run_command(args):
    logger.info('run_command() args=%r', args)


def main(argv):
    setup_logging()
    parser = create_agrument_parser()
    options, remainder = parser.parse_known_args(argv)

    is_interactive_mode = not remainder

    try:
        retcode = run_interactive() if is_interactive_mode \
            else run_command(remainder)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
        raise

    return retcode


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

