import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'wrds'
]

requires = [
    'pandas',
    'sqlalchemy',
    'psycopg2',
     # mock may need to be included if folks
     # want to run tests w/Py2
    'mock'
]

setup(
        name='wrds',
        version='3.0.6',
        description="Python access to WRDS Data",
        long_description=open('README.rst').read(),
        author='WRDS',
        author_email='wrds@wharton.upenn.edu',
        url='http://www.whartonwrds.com',
        packages=packages,
        install_requires=requires,
        package_data={
            '': ['LICENSE', 'NOTICE', '*.rst'],
            },
        classifiers=(
           'Programming Language :: Python',
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3',
           'Programming Language :: Python :: 3.5',
           'Development Status :: 4 - Beta',
           'Environment :: Console',
           'Intended Audience :: End Users/Desktop',
           'Intended Audience :: Financial and Insurance Industry',
           'Intended Audience :: Education',
           'Intended Audience :: Science/Research',
           'Topic :: Office/Business :: Financial',
           'Topic :: Scientific/Engineering :: Information Analysis',
        ),
)


