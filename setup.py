from setuptools import setup

from awsudo import VERSION


setup(
    name='awsudo',
    version=VERSION,
    description='Get temporary credentials for AWS roles.',
    url='https://github.com/pmuller/awsudo',
    author='Philippe Muller',
    author_email='philippe.muller@gmail.com',
    py_modules=['awsudo'],
    entry_points="""
        [console_scripts]
        awsudo = awsudo:main
    """,
    install_requires=['boto3 >= 1.4.0'],
    tests_require=['pytest', 'mock'],
    setup_requires=['pytest-runner'],
)
