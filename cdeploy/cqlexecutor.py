class CQLExecutor:
    def __init__(self):
        pass

    @staticmethod
    def init_table(session):
        session.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (type text, version int, PRIMARY KEY(type, version))
            WITH COMMENT = 'Schema migration history' AND CLUSTERING ORDER BY (version DESC)
        """)

    @staticmethod
    def get_top_version(session):
        return session.execute('SELECT * FROM schema_migrations LIMIT 1')

    @staticmethod
    def execute(session, script):
        statements = parse_cql(migration_section_of, script)

        for cql_statement in statements:
            print('  * Executing: {0}'.format(cql_statement))
            session.execute(cql_statement)

    @staticmethod
    def execute_undo(session, script):
        statements = parse_cql(undo_section_of, script)

        for cql_statement in statements:
            print('  * Executing: {0}'.format(cql_statement))
            session.execute(cql_statement)

    @staticmethod
    def add_schema_migration(session, version):
        session.execute("INSERT INTO schema_migrations (type, version) VALUES ('migration', {0})".format(version))

    @staticmethod
    def rollback_schema_migration(session):
        top_version = CQLExecutor.get_top_version(session)[0].version
        session.execute("DELETE FROM schema_migrations WHERE type = 'migration' AND version = {0}".format(top_version))


def parse_cql(section_func, script):
    section_to_run = section_func(script)
    collapsed_script = section_to_run.replace('\n', ' ')
    statements = [line.strip() for line in collapsed_script.split(';') if line.strip() != '']
    return statements


def migration_section_of(script):
    migration_section = ''
    for line in script.split('\n'):
        if undo_marker(line):
            break
        elif commented(line):
            continue
        else:
            migration_section += line + '\n'
    return migration_section


def undo_section_of(script):
    undo_section = ''
    in_undo = False
    for line in script.split('\n'):
        if undo_marker(line):
            in_undo = True
        elif commented(line):
            continue
        elif in_undo:
            undo_section += line + '\n'
    return undo_section


def undo_marker(line):
    return line.strip().startswith('--//@UNDO')


def commented(line):
    return line.startswith('--') or line.startswith('//')