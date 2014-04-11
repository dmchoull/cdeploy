from setuptools import setup, find_packages

setup(name='cassandra_migrations',
      version='1.0',
      packages=find_packages(),
      test_suite = "cassandra_migrations.test",
      entry_points={
          'console_scripts': [
              'cassandra_migrations = cassandra_migrations.migrator:main'
          ]
      }
)