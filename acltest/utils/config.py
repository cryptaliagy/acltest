import yaml
from absl import logging
from pydeepmerge import deep_merge
from typing import Dict, Tuple


def load_configs_from_file(file_name: str = "conf/acltest.yaml") -> Dict:
    '''
    Load a configuration from one yaml file
    '''
    configs = {}
    try:
        with open(file_name, "r") as fh:
            configs = yaml.load(fh, yaml.Loader)
    except FileNotFoundError:
        logging.warning('The file %s was not found, ignoring...', file_name)
    return configs


def merge_file_configs(*filenames: Tuple[str]) -> Dict:
    '''
    Merge all file-based configurations into one dictionary
    '''
    configs = []
    for file_name in filenames:
        configs.append(load_configs_from_file(file_name))

    return deep_merge(*configs)


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

    return configs


def get_configs_from_flags(absl_flags) -> Dict:
    '''
    Extract the configurations from files specified on the CLI and CLI configs
    '''
    cli_configs = get_cli_configs(absl_flags)
    file_configs = merge_file_configs(*absl_flags.filename)

    return deep_merge(file_configs, cli_configs)
