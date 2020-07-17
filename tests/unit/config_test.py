import pytest
from acltest.utils.config import get_cli_configs


class MockAbslFlags:
    def __init__(self,
                 pols=None,
                 defs=None,
                 policy_file=None,
                 filename=None,
                 sanitize=None,
                 svg=None,
                 output=None,
                 cleanup=True,
                 pprof_file='latest.pprof',
                 pprof_time=5):
        self.pols = pols
        self.defs = defs
        self.policy_file = policy_file
        self.filename = filename
        self.sanitize = sanitize
        self.svg = svg
        self.output = output
        self.cleanup = cleanup
        self.pprof_time = pprof_time
        self.pprof_file = pprof_file


@pytest.mark.unit
def test_get_cli_configs_pols_dir():
    expected = {
        'acl': {
            'pols_location': 'pols/',
            'defs_location': 'defs/'
        },
        'acltest': {
            'cleanup': True
        },
        'prof': {
            'pprof_time': 5,
            'pprof_file': 'latest.pprof'
        }
    }

    flags = MockAbslFlags(pols='pols/', defs='defs/', pprof_time=5)
    configs = get_cli_configs(flags)

    assert configs == expected
