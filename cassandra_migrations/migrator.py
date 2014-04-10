import os


class Migrator:
    def __init__(self, migrations_path, session):
        self.migrations_path = migrations_path
        self.session = session

    def run_migrations(self):
        for file_name in os.listdir(self.migrations_path):
            migration_file = open(os.path.join(self.migrations_path, file_name))
            migration_content = migration_file.read()
            self.session.execute(migration_content)