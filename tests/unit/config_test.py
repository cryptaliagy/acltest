import pytest
from acltest.utils.config import get_cli_configs


class MockAbslFlags:
    def __init__(self,
                 max_qps=None,
                 max_threads=None,
                 pols=None,
                 defs=None,
                 policy_file=None,
                 filename=None,
                 sanitize=None):
        self.max_qps = max_qps
        self.max_threads = max_threads
        self.pols = pols
        self.defs = defs
        self.policy_file = policy_file
        self.filename = filename
        self.sanitize = sanitize


@pytest.mark.unit
def test_get_cli_configs_pols_dir():
    expected = {
        'load': {
            'max_qps': 100,
            'max_threads': 10,
        },
        'acl': {
            'pols_location': 'pols/',
            'defs_location': 'defs/'
        },
        'acltest': {}
    }

    flags = MockAbslFlags(max_qps=100, max_threads=10, pols='pols/', defs='defs/')
    configs = get_cli_configs(flags)

    assert configs == expected
