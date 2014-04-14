import os
import sys
import yaml
from cassandra.cluster import Cluster
from cqlexecutor import CQLExecutor


class Migrator:
    def __init__(self, migrations_path, session):
        print('Reading migrations from {0}'.format(migrations_path))
        self.migrations_path = migrations_path
        self.session = session

    def run_migrations(self):
        CQLExecutor.init_table(self.session)
        top_version = self.get_top_version()

        for dir_entry in os.listdir(self.migrations_path):
            dir_entry_path = os.path.join(self.migrations_path, dir_entry)

            if not os.path.isfile(dir_entry_path):
                break

            self.apply_migration(dir_entry, top_version)

    def apply_migration(self, file_name, top_version):
        migration_script = self.read_migration(file_name)
        version = self.migration_version(file_name)

        if version > top_version:
            CQLExecutor.execute(self.session, migration_script)
            CQLExecutor.update_schema_migrations(self.session, version)
            print('  -> Migration {0} applied ({1})\n'.format(version, file_name))

    def get_top_version(self):
        result = CQLExecutor.get_top_version(self.session)
        top_version = result[0].version if len(result) > 0 else 0
        print('Current version is {0}'.format(top_version))
        return top_version

    def read_migration(self, file_name):
        migration_file = open(os.path.join(self.migrations_path, file_name))
        return migration_file.read()

    def migration_version(self, file_name):
        return int(file_name.split('_')[0])


DEFAULT_MIGRATIONS_PATH = './migrations'
CONFIG_FILE_PATH = 'config/cassandra.yml'


def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print 'Usage: cdeploy [path/to/migrations]'
        return

    migrations_path = DEFAULT_MIGRATIONS_PATH if len(sys.argv) == 1 else sys.argv[1]

    if invalid_migrations_dir(migrations_path) or missing_config(migrations_path):
        return

    config = load_config(migrations_path, os.getenv('ENV'))
    cluster = Cluster(config['hosts'])
    session = cluster.connect(config['keyspace'])

    migrator = Migrator(migrations_path, session)
    migrator.run_migrations()


def invalid_migrations_dir(migrations_path):
    if not os.path.isdir(migrations_path):
        print '"{0}" is not a directory'.format(migrations_path)
        return True
    else:
        return False


def missing_config(migrations_path):
    config_path = config_file_path(migrations_path)
    if not os.path.exists(os.path.join(config_path)):
        print 'Missing configuration file "{0}"'.format(config_path)
        return True
    else:
        return False


def config_file_path(migrations_path):
    return os.path.join(migrations_path, CONFIG_FILE_PATH)


def load_config(migrations_path, env):
    config_file = open(config_file_path(migrations_path))
    config = yaml.load(config_file)
    return config[env or 'development']


if __name__ == '__main__':
    main()