from setuptools import setup, find_packages

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split('\n')

setup(
    name="acltest",
    packages=find_packages(),
    version='0.1',
    install_requires=requirements,
    entry_points={
        'console_scripts': ['acltest = acltest.main:entry_point']
    },
)
