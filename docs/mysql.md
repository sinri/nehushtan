# Nehushtan MySQL Toolkit

## Structure

Based on `pymysql`.

* `MySQLKit` Packaged PyMySQL Connection Manager.
    * Relies on `MySQLKitConfig` as configuration definition.
* `MySQLCondition` Conditional Expression Definition.
* `MySQLQueryResult` Packaged Table Query Result.
* `MySQLTableExistence` The three points of a table or view: connection, schema and table.
    * `MySQLViewMixin` Defines readers of a table or view.
        * `MySQLTableMixin` Defines writers of a table.
            * `MySQLAnyTable` A dynamic table model definition.
        * `MySQLTableSelection` Selection Chained Reader for a class or view.

## Connect to MySQL Database

### Configuration

Write proper configuration in Python to get an instance of `MySQLKitConfig`.

By default, PyMySQL made `auto_commit` as `False`. Maybe set it as `True` is a better idea.

### Create an instance of MySQLKit

```python
# db_config : MySQLKitConfig
db = MySQLKit(db_config)
```

To reuse or package an existed instance of `Connection`, use:

```python
# connection is an instance of pymysql.connections.Connection
db = MySQLKit.make_instance_from_pymysql_connection(connection)
```

## Use raw pymysql to query

The lowest level action is to use `pymysql.connections.Connection` directly.

* def get_raw_connection(self) -> Connection

If you just want to query with a SQL, use the following...

* def raw_get_computed_sql(self, sql: str, args=None) -> str
* def raw_query_for_all_tuple_rows(self, sql: str, args=None) -> tuple
* def raw_query_for_all_dict_rows(self, sql: str, args=None) -> tuple
* def raw_query_to_modify_one(self, sql: str, args=None, commit_immediately: bool = None)
* def raw_query_to_insert_one(self, sql: str, args=None, commit_immediately: bool = None)
* def raw_query_to_modify_many(self, sql: str, args=None, commit_immediately: bool = None)
* def raw_query_to_insert_many(self, sql: str, args=None, commit_immediately: bool = None)
* def raw_execute_transaction(self, transaction_callable: Callable[["MySQLKit"], any])

Notice the `raw_execute_transaction` method。
It receives a parameter as a callable method to do with queries inside the transaction; 
when the callable successfully returns with result, it returns the result after commit;
when the callable raises any Exception, it rolls back and raise the Exception to outside.

```python
# With a simple lambda expression
inserted_id = db.raw_execute_transaction(lambda db: db.raw_query_to_insert_one('insert into ...'))
```

```python
# Or with an inner def
def act_in_transaction(db:MySQLKit):
    id=db.raw_query_to_insert_one('insert into ...')
    if id <= 0:
        raise Exception('cannot ...')
    afx=db.raw_query_to_modify_one('update ...')
    return afx

afx = db.raw_execute_transaction(act_in_transaction)
```

The above raw query methods are useful to query with SQL and optional parameters.
Simple query on single table is expected to use dynamic table model.

## Simple query with single table

Select, insert, replace, delete and update rows in one table.

### Build an instance for table model

```python
table=MySQLAnyTable(mysql_kit=db,table_name='table_name',schema_name='schema_name')
```

Amongst the parameters, `schema_name` is optional. If omitted, use the default schema defined as `db` in config. 

### Query one table

With a chained call, you can make selections on a single table.

```python
"""
select name, max(score) as max_score
from `schema_name`.`table_name`
where id > 500
group by name
order by id desc
limit 100 offset 100
"""
result = table.select_in_table() \
    .add_select_field('name') \
    .add_select_field('max(score)', 'max_score') \
    .add_condition(MySQLCondition.make_greater_than('id', '500')) \
    .set_group_by_fields(['name']) \
    .set_sort_expression('id desc') \
    .set_limit(100) \
    .set_offset(100) \
    .query_for_result_as_tuple_of_dict()
```

You can set these options:

* fields with aliases,
* conditions,
* index usages,
* group by expressions,
* order by expressions,
* limitation and offset,
* for update remark

The methods to fetch results：

* def query_for_result_as_tuple_of_dict(self)
* def query_for_result_as_tuple_of_tuple(self)

Sometimes you may meet huge amount of rows, you may use these methods to fetch with stream (i.e. without cached buffer).

* def query_for_result_stream_as_dict(self)
* def query_for_result_stream_as_tuple(self)

Those methods all return an instance of `MySQLQueryResult`.

### Modify one table

* def insert_one_row(self, row_dict: dict, commit_immediately: bool = False)
* def replace_one_row(self, row_dict: dict, commit_immediately: bool = False)
* def insert_many_rows_with_dicts(self, row_dicts: Tuple[dict], commit_immediately: bool = False)
* def replace_many_rows_with_dicts(self, row_dicts: Tuple[dict], commit_immediately: bool = False)
* def insert_many_rows_with_matrix(self, fields: tuple, row_matrix: Tuple[tuple], commit_immediately: bool = False)
* def replace_many_rows_with_matrix(self, fields: tuple, row_matrix: Tuple[tuple], commit_immediately: bool = False)
* def update_rows(self, conditions: Iterable[MySQLCondition], modifications: dict, commit_immediately: bool = False)
* def delete_rows(self, conditions: Iterable[MySQLCondition], commit_immediately: bool = False)

## Query Result

Class `MySQLQueryResult` is there.

First, check the status of result.

```python
if result.get_status() == constant.MYSQL_QUERY_STATUS_ERROR:
    # now exception should be raised
    raise Exception(f"ERROR THERE: {result.get_error()}")
# here do next work
```

There are six status constants.

```python
MYSQL_QUERY_STATUS_INIT = "INIT" # Initialized and not executed
MYSQL_QUERY_STATUS_QUERIED = "QUERIED" # Queried and fetched results in buffer, use `result.get_fetched_rows_as_tuple()` to get the tuple of rows.
MYSQL_QUERY_STATUS_EXECUTED = "EXECUTED" # Queried for modification and recorded the last inserted ID or the count of affected rows.
MYSQL_QUERY_STATUS_STREAMING = "STREAMING" # Queried and fetched the stream of rows, use `cursor=result.get_stream()` to fetch the instance of SS-Cursor class.
MYSQL_QUERY_STATUS_STREAMED = "STREAMED" # All queried rows in stream had been red, related SS-Cursor instance also closed.
MYSQL_QUERY_STATUS_ERROR = "ERROR" # Error raised, use `result.get_error()` and `result.get_sql()` to debug.
```

----

Back to [index](./index)