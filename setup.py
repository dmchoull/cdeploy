from setuptools import setup, find_packages

setup(name='cdeploy',
      version='1.0',
      packages=find_packages(),
      test_suite = "cdeploy.test",
      entry_points={
          'console_scripts': [
              'cdeploy = cdeploy.migrator:main'
          ]
      }
)