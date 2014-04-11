import unittest
from mock import *
from cassandra_migrations import Migrator
from cassandra_migrations.cql_executor import CQLExecutor

migration_1_content = open('./migrations/001_create_users.cql').read()
migration_2_content = open('./migrations/002_add_firstname.cql').read()


class ApplyingMigrationTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.migrator = Migrator('./migrations', self.session)
        self.migrator.get_top_version = Mock(return_value=0)

    def test_it_should_make_sure_the_schema_migrations_table_exists(self):
        CQLExecutor.init_table = Mock()
        self.migrator.run_migrations()
        CQLExecutor.init_table.assert_called_once_with(self.session)

    def test_it_should_initially_apply_all_the_migrations(self):
        CQLExecutor.execute = Mock()
        self.migrator.run_migrations()
        CQLExecutor.execute.assert_has_calls(
            [call(self.session, migration_1_content), call(self.session, migration_2_content)])

    def test_it_should_add_the_migration_versions_to_the_schema_migrations_table(self):
        CQLExecutor.update_schema_migrations = Mock()
        self.migrator.run_migrations()

        CQLExecutor.update_schema_migrations.assert_has_calls([call(self.session, 1), call(self.session, 2)])

    def test_it_should_only_run_migrations_that_have_not_been_applied(self):
        CQLExecutor.execute = Mock()
        self.migrator.get_top_version = Mock(return_value=1)
        self.migrator.run_migrations()

        CQLExecutor.execute.assert_called_once_with(self.session, migration_2_content)


class TopSchemaVersionTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.migrator = Migrator('./migrations', self.session)

    def test_it_should_return_zero_initially(self):
        CQLExecutor.get_top_version = Mock(return_value=[])

        self.assertEquals(0, self.migrator.get_top_version())

    def test_it_should_return_the_highest_version_from_schema_migrations(self):
        CQLExecutor.get_top_version = Mock(return_value=[Mock(version=7)])
        version = self.migrator.get_top_version()

        self.assertEquals(version, 7)


if __name__ == '__main__':
    unittest.main()