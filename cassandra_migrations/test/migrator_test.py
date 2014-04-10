import unittest
from mock import *
from cassandra_migrations import Migrator

migration_1_content = open('./migrations/001_create_users.cql').read()
migration_2_content = open('./migrations/002_add_firstname.cql').read()


class MigratorTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.execute = MagicMock()
        self.migrator = Migrator('./migrations', self.session)

    def test_it_should_make_sure_the_schema_migrations_table_exists(self):
        self.session.execute.assert_has_calls([call("""
            CREATE TABLE IF NOT EXISTS schema_migrations (type text, version int, PRIMARY KEY(type, version))
            WITH COMMENT = 'Schema migration history' AND CLUSTERING ORDER BY (version DESC)
        """)])

    def test_it_should_initially_apply_all_the_migrations(self):
        self.migrator.update_schema_migrations = Mock()
        self.migrator.run_migrations()
        self.session.execute.assert_has_calls([call(migration_1_content), call(migration_2_content)])

    def test_it_should_add_the_migration_versions_to_the_schema_migrations_table(self):
        self.migrator.apply_migration = Mock()
        self.migrator.run_migrations()
        self.session.execute.assert_has_calls([
            call("INSERT INTO schema_migrations (type, version) VALUES ('migration', 1)"),
            call("INSERT INTO schema_migrations (type, version) VALUES ('migration', 2)")
        ])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
