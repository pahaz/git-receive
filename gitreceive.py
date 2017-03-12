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
import subprocess
import os
from os.path import join, expanduser, isdir, isfile

assert sys.version_info >= (3, 4), 'require python >= 3.4'

VERSION = __version__ = '0.2.0'
ROOT_PATH = expanduser("~")
GIT_BARE_ROOT_PATH = join(ROOT_PATH, '.gitreceive.bare')
GIT_FILES_ROOT_PATH = join(ROOT_PATH, '.gitreceive.files')
COMMANDS_PATH = join(ROOT_PATH, '.gitreceive.extra.commands')
RECEIVE_HOOKS_PATH = join(ROOT_PATH, '.gitreceive.hook.receive')

USER = os.environ.get('NAME', 'anonymous')
DESCRIPTION = """
You use `git-receive` tool v{version}
Welcome!

""".format(version=VERSION)

logger = logging.getLogger('gitshell')


# utils

# def run(command):
#     output = subprocess.check_output(
#         command,
#         stderr=subprocess.STDOUT,
#         shell=True)
#     return output.decode('utf-8')


# def srun(command):
#     output = subprocess.check_output(
#         command,
#         stderr=subprocess.STDOUT)
#     return output.decode('utf-8')

def is_executable_file(path):
    return isfile(path) and os.access(path, os.X_OK)


def get_exeutable_files(path):
    return [
        file for file in os.listdir(path)
        if is_executable_file(join(path, file))
    ]


def run_all_executable_files(path, args):
    files = [join(path, x) for x in get_exeutable_files(path)]
    for file in files:
        run_executable_file(file, args)


def run_executable_file(file, args):
    logger.info('run: %r %r', file, args)
    subprocess.check_call([file] + list(args))


def clone_git_bare_repo(bare_path, destination):
    kwargs = dict(
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        cwd=destination)
    # noqa: based on https://github.com/dokku/dokku/blob/a5ac4bb08bef80339770f8c8406e1b646ddaebe6/plugins/git/functions#L26-L33
    subprocess.run(['rm', '-rf', destination])
    subprocess.run(['mkdir', '-p', destination])
    subprocess.run(['git', 'init'], **kwargs)
    subprocess.run('git config advice.detachedHead false'.split(), **kwargs)
    subprocess.run('git remote add origin'.split() + [bare_path], **kwargs)
    subprocess.run('git fetch --depth=1 origin master'.split(), **kwargs)
    subprocess.run('git reset --hard FETCH_HEAD'.split(), **kwargs)
    subprocess.run('git submodule update --init --recursive'.split(), **kwargs)
    subprocess.run('find -name .git -prune -exec rm -rf {};'.split(), **kwargs)


# commands


def git_receive_pack(line):
    "git-receive-pack"
    app_name = shlex.split(line)[0]
    app_path = join(GIT_BARE_ROOT_PATH, app_name).replace("'", '').lower()

    subprocess.check_output(["git", 'init', '--bare', app_path])
    subprocess.check_call(['git-receive-pack', app_path])

    clone_git_bare_repo(app_path, join(GIT_FILES_ROOT_PATH, app_name))

    run_all_executable_files(RECEIVE_HOOKS_PATH, [app_path])


def git_upload_pack(line):
    "git-upload-pack"
    app_name = shlex.split(line)[0]
    app_path = join(GIT_BARE_ROOT_PATH, app_name).replace("'", '').lower()

    subprocess.check_call(['git-upload-pack', app_path])

    logger.info('git-upload-pack ok')


# /commands


def prepare_root_infrastracture():
    directories = [
        GIT_BARE_ROOT_PATH, GIT_FILES_ROOT_PATH, 
        COMMANDS_PATH, RECEIVE_HOOKS_PATH]
    for directory in directories:
        if not isdir(directory):
            os.mkdir(directory)


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
    identchars = cmd.Cmd.identchars + '-'
    intro = DESCRIPTION + 'Type help or ? to list commands.\n'
    prompt = '(i-shell) $ '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_names = []

    def get_names(self):
        # This method used to pull in base class attributes
        # at a time dir() didn't do it yet.
        return dir(self.__class__) + self.extra_names

    def add_extra_command(self, name, func, hide=True, docs=None):
        setattr(self, 'do_' + name, func)
        if not hide:
            self.extra_names.append('do_' + name)
        if docs:
            func.__docs__ = docs

    def emptyline(self):
        pass

    def do_EOF(self, line):
        "exit()"
        sys.exit()

    do_q = do_quit = do_exit = do_EOF

    # last_shell_output = ''

    # def do_shell(self, line):
    #     "Run a shell command"
    #     logger.info("running shell command: %s", line)
    #     with os.popen(line) as command:
    #         output = command.read()
    #         logger.info("command output: %r", output)
    #         self.last_shell_output = output

    # def do_echo(self, line):
    #     "Print the input, replacing '$out' with the output of the last shell command"
    #     # Obviously not robust
    #     logger.info(line.replace('$out', self.last_shell_output))

    # def do_exec(self, line):
    #     "do exec()"
    #     try:
    #         logger.info(repr(exec(line, globals(), locals())))
    #     except Exception as e:
    #         logger.exception('exec error: %r', e)


def setup_cmd():
    cmd = InteractiveShell()
    commands = {
        'git-receive-pack': git_receive_pack,
        'git-upload-pack': git_upload_pack,
    }

    for name, func in commands.items():
        cmd.add_extra_command(name, func)

    extra_commands = get_exeutable_files(COMMANDS_PATH)
    for name in extra_commands:
        f = join(COMMANDS_PATH, name)
        func = lambda line, f=f: run_executable_file(f, shlex.split(line))
        cmd.add_extra_command(name, func, hide=False)
        
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
    prepare_root_infrastracture()

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

