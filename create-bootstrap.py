#!/usr/bin/env python
"""This creates a bootstrap script for general use.
The generated file, bootstrap.py can be called without any parameters. See below for some defaulted things.

The bootstrap script will contain the currently installed and available (current virtualenv or system) version of
virtualenv. When the bootstrap script runs, it will install into the virtualenv the version of pip available at that
time.
The bootstrap script will also do the following:
    1. If ~/.mytemplates/.local.autorun exists, it will be copied to the working directory.
    (This is useful for automatic activation, usage in tmux||screen||byobu, and is probably an abomination.)
    2. Defaults to using distribute instead of setuptools.
    3. If no destination directory is specified, it will set it as 'venv'.
    4. It's commented out, but it could do `pip install -r requirements.txt`. This is also an example for doing other
    things.
"""

from __future__ import print_function
import virtualenv
import textwrap
import stat
import os

venv_options = """
import os
import subprocess
import shutil

def adjust_options(options, args):
    # By default, use distribute.
    options.use_distribute = True
    # Default the destination directory to venv
    if not args:
        args.append('venv')
    # Set a sensible prompt (instead of "venv")
    if not options.prompt:
        targetdir = os.path.dirname(os.path.abspath(__file__))
        options.prompt = '({0})'.format(os.path.basename(targetdir))

def after_install(options, home_dir):
    # This could install the requirements from the get-go, but for now, skip that.
    #subprocess.call([join(home_dir, 'bin', 'pip'),
                     #'install', '-r', 'requirements.txt'])
    # Copy autorun template, if present, but don't overwrite an existing one.
    mytemplate = os.path.expanduser(join('~', '.mytemplates', '.local.autorun'))
    target = join(os.path.dirname(os.path.abspath(__file__)), '.local.autorun')
    if os.path.exists(mytemplate) and not os.path.exists(target):
        if os.path.exists(target):
            os.unlink(target)
        # Copy with user/group ownership and permissions retained as much as possible.
        shutil.copy2(mytemplate, target)
    logger.warn('\\nsource %s/bin/activate', home_dir)
"""

if __name__ == '__main__':
    with open('bootstrap.py', 'w') as outfile:
        output = virtualenv.create_bootstrap_script(textwrap.dedent(venv_options))
        outfile.write(output)
        os.fchmod(outfile.fileno(), os.fstat(outfile.fileno()).st_mode | stat.S_IEXEC)

    print('Bootstrap script written to bootstrap.py')
