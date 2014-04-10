import os


class Migrator:
    def __init__(self, migrations_path, session):
        self.migrations_path = migrations_path
        self.session = session
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (type text, version int, PRIMARY KEY(type, version))
            WITH COMMENT = 'Schema migration history' AND CLUSTERING ORDER BY (version DESC)
        """)

    def run_migrations(self):
        for file_name in os.listdir(self.migrations_path):
            migration_content = self.read_migration(file_name)
            version = self.migration_version(file_name)
            if version > self.get_top_version():
                self.apply_migration(migration_content)
                self.update_schema_migrations(version)

    def read_migration(self, file_name):
        migration_file = open(os.path.join(self.migrations_path, file_name))
        return migration_file.read()

    def migration_version(self, file_name):
        return int(file_name.split('_')[0])

    def get_top_version(self):
        pass

    def apply_migration(self, migration_content):
        self.session.execute(migration_content)

    def update_schema_migrations(self, version):
        self.session.execute("INSERT INTO schema_migrations (type, version) VALUES ('migration', {0})".format(version))
