import os

from absl import app
from absl import flags
from acltest.utils.config import get_configs_from_flags


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
    configs = get_configs_from_flags(FLAGS)
    print(configs)


def get_module_script_path(module):
    return os.path.realpath(module.__file__)


def entry_point():
    setup_flags()
    app.run(main)


if __name__ == "__main__":
    entry_point()
