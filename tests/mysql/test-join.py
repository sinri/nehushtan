from dataclasses import field

from nehushtan.mysql.MySQLAnyTable import MySQLAnyTable
from nehushtan.mysql.MySQLCondition import MySQLCondition, MySQLJoinOnCondition
from nehushtan.mysql.MySQLKit import MySQLKit

db = MySQLKit(None)


def test1():
    sql = MySQLAnyTable(mysql_kit=db, table_name="t1", schema_name="s1") \
        .select_in_table(alias="first") \
        .add_inner_join_table(table_name="t2", schema_name="s1", alias="second", on_conditions=[
        MySQLJoinOnCondition.make_field_equal(left=['first', 'f1'], right=['second', 'f1'])
    ]) \
        .add_condition(MySQLCondition.make_string_contains(field_qualifier="second", field="f3", sub_string="AW")) \
        .generate_sql()
    print(sql)


if __name__ == '__main__':
    test1()
