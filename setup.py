from setuptools import setup, find_packages


setup(
    name="acltest",
    packages=find_packages(),
    version='0.1',
    install_requires=['absl-py', 'arrow', 'capirca', 'pydeepmerge[yaml]', 'flameprof'],
    entry_points={
        'console_scripts': ['acltest = acltest.main:entry_point']
    },
)
