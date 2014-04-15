import unittest
from mock import *
from cdeploy.cqlexecutor import CQLExecutor


class CQLExecutorTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()

    def test_it_creates_the_table_if_not_existing(self):
        CQLExecutor.init_table(self.session)
        self.session.execute.assert_called_once_with("""
            CREATE TABLE IF NOT EXISTS schema_migrations (type text, version int, PRIMARY KEY(type, version))
            WITH COMMENT = 'Schema migration history' AND CLUSTERING ORDER BY (version DESC)
        """)

    def test_it_selects_the_most_recent_migration(self):
        row = []
        self.session.execute = Mock(return_value=row)

        result = CQLExecutor.get_top_version(self.session)

        self.assertEquals(row, result)
        self.session.execute.assert_called_once_with('SELECT * FROM schema_migrations LIMIT 1')

    def test_it_executes_the_migration_script(self):
        CQLExecutor.execute(self.session, 'script')
        self.session.execute.assert_called_once_with('script')

    def test_it_executes_a_multi_line_migration_script(self):
        CQLExecutor.execute(self.session, 'line1;\nline2;\n')
        self.session.execute.assert_has_calls([call('line1'), call('line2')])

    def test_it_multi_line_statements(self):
        CQLExecutor.execute(self.session, 'statement start\nmore statement\nend statement;\nstatement\n2')
        self.session.execute.assert_has_calls([call('statement start more statement end statement'), call('statement 2')])

    def test_it_ignores_comments(self):
        CQLExecutor.execute(self.session, 'line1;\n--comment\n//comment\nline2')
        self.session.execute.assert_has_calls([call('line1'), call('line2')])

    def test_it_updates_schema_migrations_with_the_migration_version(self):
        CQLExecutor.update_schema_migrations(self.session, 10)
        self.session.execute.assert_called_once_with(
            "INSERT INTO schema_migrations (type, version) VALUES ('migration', 10)")


if __name__ == '__main__':
    unittest.main()
