# db_error_handling #

## How to Run ##
1. Create a virtualenv with python 2.7 and activate it. If you don't know how: 
    `virtualenv --python=/usr/bin/python2.7 <path/to/new/virtualenv/>`
    
    `cd <path/to/new/virtualenv>` 
    
    `source activate`
2. `git clone https://github.com/Nerdenator/db_error_handling`
3. `cd db_error_handling`
4. `pip install -r requirements.txt`
5. `python`
6. `>>> from db_app.models import *`
7. `>>> setup_table()`
8. You now have a table with contents.

## Now what? ##
This repository is meant as a template for how to best handle errors with multiple database transactions.
In this project (and another project much more complex than this, and proprietary), we have a table with three fields:

* a `value1` field: a simple integer
* a `value2` field: a simple integer
* a `same` field: a char field that has a max length of 3 characters

We then have methods to manipulate the `same` field, and to demonstrate exception behavior:

* `set_yes()`: a method that checks `value1` and `value2` columns in the row. If these two columns have the same value within them,
`set_yes()` will then set the contents of the `same` column in that row to `yes` using a `transaction.atomic()` context manager with exception-handling logic.
* `set_no()`: a method that checks `value1` and `value2` columns in the row. If these two columns have different values within them,
`set_no()` will then set the contents of the `same` column in that row to `no` using a `transaction.atomic()` context manager with exception-handling logic.
* `broken_query()`: a method that is meant to try to run a statement on the database that will result in an exception being thrown.
In this case, it tries to set the contents of a column that doesn't exist in the table using a `transaction.atomic()` context manager with exception-handling logic.
* `bulk_set()`: Runs `set_yes()`, `set_no()`, and `broken_query()`, in that order, all within a `try-except-finally` statement.
* `reset_table()`: a method that sets the `same` column to have a null value in all rows. 
* `print_table()`: uses a Pandas dataframe to pretty-print the database table in the python console.
* `setup_table()`: uses the Django ORM to put values in the table. Only needs to be run once.

## What are we trying to solve? ##
Let's say a client wants to make sure that the `same` column always has an appropriate value in it, and that there aren't any weird things going on in the table.
If we run `bulk_set()`, `set_yes()` and `set_no()` will run without issue, but `broken_query()` will not. Since one of the functions did not execute properly, the client
has said that they want _all_ of the changes made by `set_yes()` and `set_no()` to be rolled back. How would you go about achieving this?