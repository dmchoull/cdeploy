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
        session.execute('SELECT * FROM schema_migrations LIMIT 1')

    @staticmethod
    def execute(session, script):
        session.execute(script)

    @staticmethod
    def update_schema_migrations(session, version):
        session.execute("INSERT INTO schema_migrations (type, version) VALUES ('migration', {0})".format(version))