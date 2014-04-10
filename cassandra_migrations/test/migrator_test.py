import unittest
from mock import *
from cassandra_migrations import Migrator

migration_1_content = open('./migrations/001_create_users.cql').read()
migration_2_content = open('./migrations/002_add_firstname.cql').read()


class ApplyingMigrationTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.session.execute = Mock()
        self.migrator = Migrator('./migrations', self.session)
        self.migrator.get_top_version = Mock(return_value=0)

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

    def test_it_should_only_run_migrations_that_have_not_been_applied(self):
        self.migrator.update_schema_migrations = Mock()
        self.session.execute.reset_mock()
        self.migrator.get_top_version = Mock(return_value=1)
        self.migrator.run_migrations()

        self.session.execute.assert_called_once_with(migration_2_content)


class TopSchemaVersionTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.migrator = Migrator('./migrations', self.session)

    def test_it_should_return_zero_initially(self):
        self.session.execute = Mock(return_value=[])

        self.assertEquals(0, self.migrator.get_top_version())

    def test_it_should_return_the_highest_version_from_schema_migrations(self):
        self.session.execute = Mock(return_value=[Mock(version=7)])
        version = self.migrator.get_top_version()

        self.session.execute.assert_called_with('SELECT * from schema_migrations LIMIT 1')
        self.assertEquals(version, 7)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
