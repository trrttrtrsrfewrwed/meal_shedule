from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from CONSTS import *
import json


def add(table_name, dict_, cur):
    query = '''INSERT INTO {} (name, "data") VALUES (%s, %s)'''
    for key, value in dict_.items():
        cur.execute(query.format(table_name), (key, json.dumps(value)))


def update_notifier(json_notifier):
    query = """UPDATE {} SET notifier = %s"""
    with connect(**database_params) as conn:
        cur = conn.cursor()
        cur.execute(query.format(NOTIFIER_TABLE_NAME), (json.dumps(json_notifier), ))
        cur.close()


def get_notifier():
    query = """SELECT * FROM {}""".format(NOTIFIER_TABLE_NAME)
    with connect(**database_params) as conn:
        cur = conn.cursor()
        cur.execute(query)
        answer = cur.fetchone()[0]
        cur.close()
    return answer


def get_names(table_name):
    query = """SELECT name
                FROM {}""".format(table_name)
    with connect(**database_params) as conn:
        cur = conn.cursor()
        cur.execute(query.format(table_name))
        answer = [k[0] for k in cur.fetchall()]
        cur.close()
    return answer


def get(table_name, name):
    query = """SELECT "data"
               FROM {}
               WHERE name = {}"""
    with connect(**database_params) as conn:
        cur = conn.cursor()
        cur.execute(query.format(table_name, name))
        answer = cur.fetchall()[0][0]
        cur.close()
    return answer


def create_database():
    with connect(**database_params) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute('CREATE DATABASE ' + DATABASE_NAME)
        cur.close()
        database_params['dbname'] = DATABASE_NAME


def drop_database():
    with connect(**database_params) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute('DROP DATABASE ' + DATABASE_NAME)
        cur.close()


def create_tables():
    with connect(**database_params) as conn:
        cur = conn.cursor()
        for table_name in TABLE_NAMES:
            cur.execute('DROP TABLE IF EXISTS {}'.format(table_name))

            cur.execute('''
                        CREATE TABLE {} (
                            name VARCHAR(255),
                            "data" json
                        )
                   '''.format(table_name))
            add(table_name, dicts[table_name], cur)
        cur.execute('DROP TABLE IF EXISTS {}'.format(NOTIFIER_TABLE_NAME))

        cur.execute('''
                                CREATE TABLE {} (
                                    notifier json
                                )
                           '''.format(NOTIFIER_TABLE_NAME))
        cur.execute("""INSERT INTO {} VALUES (%s)""".format(NOTIFIER_TABLE_NAME),
                    ('{"schedule": {}, "product_counter": {}}', ))
        cur.close()
