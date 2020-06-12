import capirca
import subprocess
import os

from absl import app
from absl import flags
from absl import logging
# from acltest.utils.config import get_configs_from_flags


FLAGS = flags.FLAGS


def setup_flags():
    flags.DEFINE_multi_string(
        'filename',
        ['conf/acltest.yaml'],
        'Configuration input file(s)',
        short_name='f'
    )

    flags.DEFINE_integer(
        'max_qps',
        None,
        'Maximum number of queries per second to spawn',
        short_name='q'
    )
    flags.DEFINE_integer(
        'max_threads',
        None,
        'Maximum number of threads to use',
        short_name='t'
    )
    flags.DEFINE_string(
        'pols',
        None,
        'Location of the policies folder',
        short_name='p'
    )
    flags.DEFINE_string(
        'defs',
        None,
        'Location of the definitions folder',
        short_name='d'
    )
    flags.DEFINE_string(
        'policy_file',
        None,
        'Location to a single policy file to render'
    )


def main(argv):
    del argv
    # configs = get_configs_from_flags(FLAGS)
    capirca_install_path = get_module_script_path(capirca) + "/aclgen.py"
    subprocess_profile_script(
        capirca_install_path,
        # Capirca can only use 1 renderer for flamegraph testing
        # as cProfiler and multiprocessing don't play nice together
        script_args=['--max_renderers', '1']
    )


def subprocess_profile_script(script_path, script_args=[]):
    logging.info(
        "script_path: %s\nscript_args: %s",
        script_path,
        script_args
    )
    return subprocess.call([
        'python',
        '-m',
        'flamegraph',
        '-o',
        'perf.log',
        script_path,
        *script_args
    ])


def get_module_script_path(module):
    return os.path.dirname(module.__file__)


def entry_point():
    setup_flags()
    app.run(main)


if __name__ == "__main__":
    entry_point()
