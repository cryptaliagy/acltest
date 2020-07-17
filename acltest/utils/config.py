from pydeepmerge import (
    deep_merge,
    merge_configs
)
from typing import (
    Dict,
)


def get_cli_configs(absl_flags) -> Dict:
    configs = {
        'acl': {},
        'prof': {},
        'acltest': {}
    }

    if absl_flags.policy_file:
        configs['acl']['policy_file'] = absl_flags.policy_file
    elif absl_flags.pols:
        configs['acl']['pols_location'] = absl_flags.pols

    if absl_flags.defs:
        configs['acl']['defs_location'] = absl_flags.defs

    if absl_flags.sanitize:
        configs['acltest']['sanitize'] = absl_flags.sanitize

    if absl_flags.svg or absl_flags.output is not None:
        configs['acltest']['svg'] = True

    if absl_flags.output:
        configs['acltest']['doc_output'] = absl_flags.output

    if absl_flags.cleanup is not None:
        configs['acltest']['cleanup'] = absl_flags.cleanup

    if absl_flags.pprof_time is not None:
        configs['prof']['pprof_time'] = absl_flags.pprof_time

    return configs


def get_configs_from_flags(absl_flags) -> Dict:
    '''
    Extract the configurations from files specified on the CLI and CLI configs
    '''
    default_configs = {
        'acl': {
            'defs_location': 'defs',
            'pols_location': 'policies'
        },
        'prof': {
            'pprof_file': 'latest.pprof',
            'pprof_time': 5
        },
        'acltest': {
            'doc_output': 'latest',
            'cleanup': True,
            'svg': False,
            'sanitize': False
        }
    }
    cli_configs = get_cli_configs(absl_flags)
    file_configs = merge_configs(*absl_flags.filename, strict=True)

    return deep_merge(default_configs, file_configs, cli_configs)
