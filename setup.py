from setuptools import setup, find_packages

setup(name='cdeploy',
      version='0.8',
      packages=find_packages(),
      test_suite = "cdeploy.test",
      entry_points={
          'console_scripts': [
              'cdeploy = cdeploy.migrator:main'
          ]
      }
)