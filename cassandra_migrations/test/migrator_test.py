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

    def test_it_should_initially_apply_all_the_migrations(self):
        self.migrator.run_migrations()

        expected = [call(migration_1_content), call(migration_2_content)]
        self.assertEqual(self.session.execute.call_args_list, expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
