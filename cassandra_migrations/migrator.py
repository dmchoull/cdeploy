import os
import sys
import yaml
from cassandra.cluster import Cluster
from cassandra_migrations.cql_executor import CQLExecutor

DEFAULT_MIGRATIONS_PATH = './migrations'
CONFIG_PATH = 'config/cassandra.yml'


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
            print(' -> Migration {0} applied ({1})'.format(version, file_name))

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


def main():
    migrations_path = DEFAULT_MIGRATIONS_PATH if len(sys.argv) == 1 else sys.argv[1]

    config = load_config(migrations_path)

    cluster = Cluster(config['hosts'])
    session = cluster.connect(config['keyspace'])
    migrator = Migrator(migrations_path, session)
    migrator.run_migrations()


def load_config(migrations_path):
    config_file = open(os.path.join(migrations_path, CONFIG_PATH))
    config = yaml.load(config_file)
    return config


if __name__ == '__main__':
    main()