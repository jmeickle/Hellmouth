# Manages in-game databases. Currently, uses SQLite 3.

import sqlite3

# Creates a connection when this module is first imported.
class Database(object):
    connection = sqlite3.connect(':memory:')

# Execute a query against the database. Only return results if committing.
def query(q, args=()):
    cur = Database.connection.cursor()
    cur.execute(q, args)
    Database.connection.commit()
    return cur.fetchall()

# List the tables in the database.
def list_tables(): 
    return [x[0] for x in query("SELECT name FROM sqlite_master WHERE type = 'table'")]

# Save the entire database to a .sql dump file.
def dump(filename):
    with open(filename+".sql", 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)

# Save a list of tables into .sql dump files matching a pattern.
def dump_tables(tables, filename):
    db_tables = list_tables()
    for table in tables:
        assert table in db_tables
        with open(filename+"_%s.sql" % table, 'w') as f:
            for line in _iterdump(Database.connection, table):
                f.write('%s\n' % line)

# The below is modified from: http://stackoverflow.com/a/6677833

# Mimic the sqlite3 console shell's .dump command
# Author: Paul Kippes <kippesp@gmail.com>

def _iterdump(connection, table_name):
    """
    Returns an iterator to the dump of the database in an SQL text format.

    Used to produce an SQL dump of the database.  Useful to save an in-memory
    database for later restoration.  This function should not be called
    directly but instead called from the Connection method, iterdump().
    """

    cu = connection.cursor()
    table_name = table_name

    yield('BEGIN TRANSACTION;')

    # sqlite_master table contains the SQL CREATE statements for the database.
    q = """
       SELECT name, type, sql
        FROM sqlite_master
            WHERE sql NOT NULL AND
            type == 'table' AND
            name == ?
        """
    schema_res = cu.execute(q, (table_name,))
    for table_name, type, sql in schema_res.fetchall():
        if table_name == 'sqlite_sequence':
            yield('DELETE FROM sqlite_sequence;')
        elif table_name == 'sqlite_stat1':
            yield('ANALYZE sqlite_master;')
        elif table_name.startswith('sqlite_'):
            continue
        else:
            yield('%s;' % sql)

        # Build the insert statement for each row of the current table
        res = cu.execute("PRAGMA table_info('%s')" % table_name)
        column_names = [str(table_info[1]) for table_info in res.fetchall()]
        q = "SELECT 'INSERT INTO \"%(tbl_name)s\" VALUES("
        q += ",".join(["'||quote(" + col + ")||'" for col in column_names])
        q += ")' FROM '%(tbl_name)s'"
        query_res = cu.execute(q % {'tbl_name': table_name})
        for row in query_res:
            yield("%s;" % row[0])

    yield('COMMIT;')

# Restore a .sql dump file to memory.
def restore(filename):
    with open(filename+".sql", 'r') as f:
        Database.connection.cursor().executescript(f.read())
        Database.connection.commit()

# Basic database testing.
if __name__ == '__main__':

    print "Creating tables."
    query("CREATE TABLE IF NOT EXISTS item (iid int, PRIMARY KEY (iid))")
    query("CREATE TABLE IF NOT EXISTS inventory (aid int, root int, depth int, PRIMARY KEY (aid))")
    query("CREATE TABLE IF NOT EXISTS inventory_item (aid int, iid int)")
    query("CREATE TABLE IF NOT EXISTS item_tag (iid int, tid int, detail int, tag text)")

    tables = list_tables()

    print "Existing tables: %s" % list_tables()
 
    # Dump the tables to files.
    print "Dumping tables."
    filename = 'test'
    dump_tables(tables, filename)

    print "Dropping tables."
    for table in tables:
        query('DROP TABLE IF EXISTS %s' % table)

    print "Existing tables: %s" % list_tables()

    print "Restoring tables."
    for table in tables:
        restore(filename+"_%s" % table)

    print "Existing tables: %s" % list_tables()