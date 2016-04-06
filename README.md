**This repo is not being maintained - please use the fork at: https://github.com/rackerlabs/cdeploy**

cdeploy
=======

cdeploy is a simple tool to manage your Cassandra schema migrations in the style of [dbdeploy](http://dbdeploy.com/)

Installation
=====

```pip install cdeploy```

Usage
=====

By default, cdeploy will look for migrations in './migrations'. This can be overridden by passing the path to your migrations directory as the first argument:

    cdeploy db/migrations

The migrations directory should contain CQL scripts using the following naming convention: [version]_migration_description.cql

For example:

    migrations/
        001_create_orders_table.cql
        002_create_customers_table.cql

Version numbers should begin from 1. Migration scripts may contain multiple semicolon terminated CQL statements. Comment lines can begin with either "--" or "//".

Migrations can also specify how to revert the changes by including additional statements following a line containing "--//@UNDO". For example:

    CREATE TABLE orders(
        order_id uuid PRIMARY KEY,
        price text
    );
    
    --//@UNDO
    
    DROP TABLE orders;

To undo the most recently applied migration, run:

    cdeploy --undo

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
