import arrow
import capirca
import pathlib
import re
import subprocess
import os

from absl import app
from absl import flags
from absl import logging
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
    flags.DEFINE_boolean(
        'sanitize',
        None,
        'Sanitize output svg'
    )


def main(argv):
    del argv
    configs = get_configs_from_flags(FLAGS)
    capirca_install_path = get_module_script_path(capirca) + "/aclgen.py"
    subprocess_profile_script(
        capirca_install_path,
        # Capirca can only use 1 renderer for flamegraph testing
        # as cProfiler and multiprocessing don't play nice together
        script_args=['--max_renderers', '1'],
        sanitize=configs['acltest']['sanitize']
    )


def subprocess_profile_script(script_path, script_args=[], sanitize=True):
    logging.info(
        "script_path: %s\nscript_args: %s",
        script_path,
        script_args
    )
    file_name = arrow.now().format('YYYY-MM-DD-HH:mm:ss-ZZ')
    profile = subprocess.call([
        'python',
        '-m',
        'cProfile',
        '-o',
        'perf/%s.prof' % file_name,
        script_path,
        *script_args
    ])

    flamegraph_convert = subprocess.call([
        'flameprof',
        '-o',
        'flamegraph/%s.plog' % file_name,
        '--format',
        'log',
        'perf/%s.prof' % file_name
    ])

    with open('flamegraph/%s.svg' % file_name, 'w') as f:
        flamegraph = subprocess.call([
            'flamegraph.pl',
            '--title="%s cProfile"' % file_name,
            'flamegraph/%s.plog' % file_name,
        ], stdout=f)
    with open('flamegraph/%s_inverted.svg' % file_name, 'w') as f:
        inverted_flamegraph = subprocess.call([
            'flamegraph.pl',
            '--title="%s cProfile"' % file_name,
            '--inverted',
            '--reverse',
            'flamegraph/%s.plog' % file_name,
        ], stdout=f)

    try:
        os.remove('docs/latest.svg')
        os.remove('docs/latest_inverted.svg')
    except Exception:
        pass

    subprocess.call([
        'cp',
        'flamegraph/%s.svg' % file_name,
        'docs/latest.svg'
    ])

    subprocess.call([
        'cp',
        'flamegraph/%s_inverted.svg' % file_name,
        'docs/latest_inverted.svg'
    ])

    if sanitize:
        sanitize_file('docs/latest.svg', r'/\.virtual.*/site-packages/')
        sanitize_file('docs/latest_inverted.svg', r'/\.virtual.*/site-packages/')

    for f in pathlib.Path('.').glob('sample_*'):
        f.unlink()

    return (profile, flamegraph_convert, flamegraph, inverted_flamegraph)


def get_module_script_path(module):
    return os.path.dirname(module.__file__)


def sanitize_file(file_name, regexp):
    with open(file_name, 'r') as f:
        data = f.read()

    sanitized = re.sub(regexp, '', data)

    with open(file_name, 'w') as f:
        f.write(sanitized)


def entry_point():
    setup_flags()
    app.run(main)


if __name__ == "__main__":
    entry_point()
