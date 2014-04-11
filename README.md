cdeploy
=======

cdeploy is a simple tool to manage your Cassandra schema migrations.

Installation
=====

Coming soon to pip

Usage
=====

By default, cdeploy will look for migrations in './migrations'. This can be overridden by passing the path to your migrations directory as the first argument:

    cdeploy db/migrations

The migrations directory should contain CQL scripts using the following naming convention: [version]_migration_description.cql

For example:

    migrations/
        001_create_orders_table.cql
        002_create_customers_table.cql

Version numbers should begin from 1. Migration scripts may contain multiple semicolon terminated CQL statements.

Configuration
====

cdeploy will look in your migrations directory for a configuration file named cassandra.yml, in a subdirectory named config:

    migrations/
       config/
           cassandra.yml

The configuration file specifies the hosts to connect to and the keyspace name, and supports multiple environments. For example:

    development:
        hosts: [host1]
        keyspace: keyspace_name
    
    production:
        hosts: [host1, host2, host3]
        keyspace: keyspace_name

The environment can be set via the ENV shell variable, and defaults to development if not specified:

    ENV=production cdeploy

TODO
====
 * Migration rollback
 * Rollup migrations to establish a new baseline
