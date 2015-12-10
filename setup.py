try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

setup(
        name="wrds",
        version='0.0.5',
        description="Read SAS datasets remotely (from wrds-cloud) into a Pandas dataframe.",
        author="Joe Dougherty",
        author_email="josepd@wharton.upenn.edu",
        url="https://github.com/wharton/wrds",
        packages=['wrds'],
        install_requires=['jaydebeapi', 'pandas'],
)

