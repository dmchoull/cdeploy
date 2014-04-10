import unittest
from mock import *
from cassandra_migrations import Migrator


class MigratorTests(unittest.TestCase):
    def test_it_should_initially_apply_all_the_migrations(self):
        session = MagicMock()
        session.execute = MagicMock()

        migrator = Migrator('./migrations', session)
        migrator.run_migrations()

        expected = [call('CREATE TABLE users'), call('ALTER TABLE users ADD firstname text')]
        self.assertEqual(session.execute.call_args_list, expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
