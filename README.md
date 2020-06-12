# AclTest
![build status](https://github.com/taliamax/acltest/workflows/acltest/build/badge.svg)


It is highly recommended to use the python package `pre-commit` as it will ensure all commits pass the lint.

```bash
$ pip install pre-commit
$ pre-commit install
```

An install script has been included to install all requirements and all test requirements, as well as running the test suite for a baseline. Optionally, this can also install pre-commit hooks if you pass the `--hooks` flag

```bash
$ ./install  # no pre-commit hooks
# ./install --hooks  # with pre-commit hooks
```

An uninstall script has also been included. It also accepts the `--hooks` flag to uninstall pre-commit and its dependencies.

```bash
$ ./uninstall  # uninstalls just acltest and its dependencies
$ ./uninstall --hooks  # uninstalls pre-commit hooks as well as acltest
```
