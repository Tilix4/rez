"""
Command line interface for interacting with Launcher using Rez.
"""

from rez.cli._main import SetupRezSubParser
import sys


def setup_parser(parser, completions=False):

    subparsers = parser.add_subparsers(dest='launcher_subcommand')

    for subcommand in ["env", "bake", "update", "sync", "list", "find", "cat"]:
        subparser = subparsers.add_parser(subcommand, setup_subparser=SetupRezSubParser("rez.contrib.animallogic.launcher.cli." + subcommand))


def get_command_function_from_module(module_name):

    try:
        __import__(module_name, globals(), locals(), [], -1)
    except Exception, e:
        return None

    module = sys.modules[module_name]

    return getattr(module, 'command')


def command(opts, parser, extra_arg_groups=None):

    module_name = "rez.contrib.animallogic.launcher.cli.%s" % opts.launcher_subcommand
    func = get_command_function_from_module(module_name)
    func(opts, parser, extra_arg_groups)