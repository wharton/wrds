try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

setup(
        name="wrds",
        version='0.0.5',
        description="Connect to wrds-cloud locally.",
        author="Joe Dougherty",
        author_email="josepd@wharton.upenn.edu",
        url="https://github.com/wharton/wrds",
        packages=['wrds'],
        install_requires=['jaydebeapi', 'pandas'],
)

