from setuptools import setup, find_packages

setup(
    name='cdeploy',
    version='0.8',
    description='A tool for managing Cassandra schema migrations',
    author='David McHoull',
    author_email='dmchoull@gmail.com',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    url='https://github.com/dmchoull/cdeploy',
    download_url='https://github.com/dmchoull/cdeploy/archive/v0.8.tar.gz',
    keywords=['cassandra', 'migrations'],
    packages=find_packages(),
    install_requires=['PyYAML', 'cassandra-driver'],
    tests_require=['mock'],
    test_suite="cdeploy.test",
    entry_points={
        'console_scripts': [
            'cdeploy = cdeploy.migrator:main'
        ]
    }
)