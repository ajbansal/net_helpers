from setuptools import setup
from os import path
import sys

here = path.abspath(path.dirname(__file__))
sys.path.insert(0, path.join(here, "net_helpers"))

import __version__ as version


def readme():
    with open('README.rst') as f:
        return f.read()


download_url = 'https://github.com/ajbansal/net_helpers/archive/{}.tar.gz'.format(version.package_version)

setup(name='net_helpers',
      version=version.package_version,
      long_description=readme(),
      test_suite='nose.collector',
      tests_require=['nose'],
      description='A collection of utilities for working with net '
                  'frameworks like ftp/sftp, ssh, ldap jira, jama, jenkins etc',
      url='https://github.com/ajbansal/net_helpers',
      author='Abhijit Bansal',
      author_email='pip@abhijitbansal.com',
      license='MIT',
      packages=[],
      scripts=[],
      entry_points={},
      package_data={},
      zip_safe=False,
      install_requires=[],
      keywords=[],
      include_package_data=True,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
      ],
      )
