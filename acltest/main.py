import arrow
import pathlib
import pstats
import subprocess
import os

from absl import app
from absl import flags
from absl import logging
from acltest.utils.config import get_configs_from_flags
from functools import singledispatch


FLAGS = flags.FLAGS


def setup_flags():
    flags.DEFINE_multi_string(
        'filename',
        ['conf/acltest.yaml'],
        'Configuration input file(s)',
        short_name='f'
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
    flags.DEFINE_boolean(
        'svg',
        None,
        'Export the svg to the docs folder.\n(default: \'false\')'
    )
    flags.DEFINE_string(
        'output',
        None,
        'Name of the resulting svg output in the docs folder. Implies --svg.' +
        '\n(default: \'latest\')',
        short_name='o'
    )
    flags.DEFINE_boolean(
        'cleanup',
        None,
        'Flag to determine if cleanup of the output files should happen'
    )
    flags.DEFINE_integer(
        'pprof_time',
        None,
        'Length of time that the profiling thread in capirca should run for.\n(default: 5)'
    )


def make_capirca_args_from_config(config):
    result = ['--max_renderers', '1']  # needed because of multiprocessing
    if 'pols_location' in config['acl']:
        result.append('--base_directory')
        result.append(config['acl']['pols_location'])

    if 'defs_location' in config['acl']:
        result.append('--definitions_directory')
        result.append(config['acl']['defs_location'])

    if 'pprof_time' in config['prof']:
        result.append('--profile_time')
        result.append(str(config['prof']['pprof_time']))

    return result


def main(argv):
    del argv
    configs = get_configs_from_flags(FLAGS)
    script_args = make_capirca_args_from_config(configs)

    subprocess_profile_script(
        'aclgen',
        script_args=script_args,
        make_doc=configs['acltest']['svg'],
        docs_output=configs['acltest']['doc_output'],
        sanitize=configs['acltest']['sanitize'],
        cleanup=configs['acltest']['cleanup']
    )


@singledispatch
def clean_all_dir_files(directory):
    for document in directory.iterdir():
        if document.is_dir():
            clean_all_dir_files(document)
        if document.is_file():
            document.unlink()


@clean_all_dir_files.register
def _(directory: str):
    path_obj = pathlib.Path(directory)
    clean_all_dir_files(path_obj)


def subprocess_profile_script(
        script_name,
        script_args=[],
        make_doc=False,
        docs_output='latest',
        sanitize=True,
        cleanup=True
):
    logging.info(
        "script_path: %s\nscript_args: %s",
        script_name,
        script_args
    )
    file_name = arrow.now().format('YYYY-MM-DD-HH:mm:ss-ZZ')
    subprocess.call([
        script_name,
        '--profile_file',
        'perf/%s.prof' % file_name,
        '--output_directory',
        'output',
        '--pprof_file',
        'pprof/%s.pprof' % file_name,
        *script_args
    ])

    if cleanup:
        clean_all_dir_files('output')

    if sanitize:
        (pstats.Stats('perf/%s.prof' % file_name)
         .strip_dirs()
         .dump_stats('perf/%s.prof' % file_name))

    subprocess.call([
        'flameprof',
        '-o',
        'flamegraph/%s.plog' % file_name,
        '--format',
        'log',
        'perf/%s.prof' % file_name
    ])

    with open('flamegraph/%s.svg' % file_name, 'w') as f:
        subprocess.call([
            'flamegraph.pl',
            '--title="%s cProfile"' % file_name,
            'flamegraph/%s.plog' % file_name,
        ], stdout=f)
    with open('flamegraph/%s_inverted.svg' % file_name, 'w') as f:
        subprocess.call([
            'flamegraph.pl',
            '--title="%s cProfile"' % file_name,
            '--inverted',
            '--reverse',
            'flamegraph/%s.plog' % file_name,
        ], stdout=f)
    if make_doc:
        try:
            os.remove('docs/%s.svg' % docs_output)
            os.remove('docs/%s.svg' % docs_output)
        except Exception:
            pass

        subprocess.call([
            'cp',
            'flamegraph/%s.svg' % file_name,
            'docs/%s.svg' % docs_output
        ])

        subprocess.call([
            'cp',
            'flamegraph/%s_inverted.svg' % file_name,
            'docs/%s_inverted.svg' % docs_output
        ])

        subprocess.call([
            'go',
            'tool',
            'pprof',
            '-svg',
            '-output',
            'docs/%s_pprof.svg' % docs_output,
            'pprof/%s.pprof' % file_name
        ])

    return file_name


def get_module_script_path(module):
    return os.path.dirname(module.__file__)


def entry_point():
    setup_flags()
    app.run(main)


if __name__ == "__main__":
    entry_point()
