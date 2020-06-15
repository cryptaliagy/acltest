from pydeepmerge import (
    deep_merge,
    merge_configs
)
from typing import (
    Dict,
)


def get_cli_configs(absl_flags) -> Dict:
    configs = {
        'load': {},
        'acl': {},
    }

    if absl_flags.max_qps:
        configs['load']['max_qps'] = absl_flags.max_qps
    if absl_flags.max_threads:
        configs['load']['max_threads'] = absl_flags.max_threads

    if absl_flags.policy_file:
        configs['acl']['policy_file'] = absl_flags.policy_file
    elif absl_flags.pols:
        configs['acl']['pols_location'] = absl_flags.pols

    if absl_flags.defs:
        configs['acl']['defs_location'] = absl_flags.defs

    if absl_flags.sanitize:
        configs['acltest']['sanitize'] = absl_flags.sanitize

    return configs


def get_configs_from_flags(absl_flags) -> Dict:
    '''
    Extract the configurations from files specified on the CLI and CLI configs
    '''
    cli_configs = get_cli_configs(absl_flags)
    file_configs = merge_configs(*absl_flags.filename, strict=True)

    return deep_merge(file_configs, cli_configs)
