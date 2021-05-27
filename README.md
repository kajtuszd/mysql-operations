# mysql-operations

## Prerequisites

In order to create appropriate correct dataset.

- First database should be named `employees`.
Database without titles table should be named: `employees_copy`.

- Install `Docker` & `Docker-Compose`, configure access without `sudo` command.
- Install MySQL.

## Configure app

### Create databases

Import dump from [repo](https://github.com/datacharmer/test_db):

```shell
git clone https://github.com/datacharmer/test_db
```

Enter directory:

```shell
cd test_db/
```

Create `employees` database from dump:

```shell
mysql < employees.sql -u [user] -p[password]
```

Create empty database `employees_copy`:

```shell
mysqladmin create employees_copy -u [user] -p[password]
```

Make sure `employees.sql` dump exist:

```shell
mysqldump employees > employees.sql -u [user] -p[password]
```

Import content of `employees` to `employees_copy`:

```shell
mysql employees_copy < employees.sql -u [user] -p[password]
```

Log into mysql console:

```shell
mysql -u [user] -p[password]
```

Check if databases `employees` and `employees_copy` exist:

```shell
mysql> show databases;
```

```shell
+--------------------+
| Database           |
+--------------------+
| information_schema |
| employees          |
| employees_copy     |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
6 rows in set (0,00 sec)
```

Result should be similar.

Next remove table titles from `employees_copy`.

```shell
mysql> use employees_copy; drop table titles;
```

```shell
mysql> show tables from employees;
+----------------------+
| Tables_in_employees  |
+----------------------+
| current_dept_emp     |
| departments          |
| dept_emp             |
| dept_emp_latest_date |
| dept_manager         |
| employees            |
| salaries             |
| titles               |
+----------------------+
8 rows in set (0,01 sec)

mysql> show tables from employees_copy;
+--------------------------+
| Tables_in_employees_copy |
+--------------------------+
| current_dept_emp         |
| departments              |
| dept_emp                 |
| dept_emp_latest_date     |
| dept_manager             |
| employees                |
| salaries                 |
+--------------------------+
7 rows in set (0,00 sec)
```

Log out of MySQL console.

Create dump of `employees_copy_dump`:

```shell
mysqldump employees_copy > employees_copy.sql -u [user] -p[password]
```

Rename dumps to `employees_dump.sql` and `employees_copy_dump.sql`.

Move `employees_dump.sql` to `./data/sql1/`.

Move `employees_copy_dump.sql` to `./data/sql2/`.

```shell
.
├── code
│   ├── entrypoint.sh
│   ├── main.py
│   ├── test_database_post.py
│   └── test_database_pre.py
├── data
│   ├── sql1
│   │   └── employees_dump.sql
│   └── sql2
│       └── employees_copy_dump.sql
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── template.env

```

### Set environment variables in file `.env`

Copy template:

```shell
cp template.env .env 
```

Set variables as following:

```shell
HOST_1=mysql1
DATABASE_1=employees
DB_PORT_1=3307
HOST_2=mysql2
DATABASE_2=employees_copy
DB_PORT_2=3308
APP_PORT=8000
```

Add your own data to the rest of variables:

```shell
USER_1=TYPE_YOUR_USER
MYSQL_HOST_1=TYPE_YOUR_HOST
PASSWORD_1=TYPE_YOUR_PASSWORD
MYSQL_ROOT_PASSWORD_1=TYPE_YOUR_PASSWORD
USER_2=TYPE_YOUR_USER
MYSQL_HOST_2=TYPE_YOUR_HOST
PASSWORD_2=TYPE_YOUR_PASSWORD
MYSQL_ROOT_PASSWORD_2=TYPE_YOUR_PASSWORD
```

## Run app

```shell
docker-compose up
```

Stop app:

```shell
^C
docker-compose down
```

## Description

### Jobs

App consists of two database containers and one app container.

Important fact is that dump `.sql` files are moved through volume mount inside directory where `.sql` scripts initialize database.

```yaml
volumes:
    - ./data/sql2:/docker-entrypoint-initdb.d/
```

App container is waiting until database containers work. Then `test_database_pre.py` scripts are run in order to check correctness of input data. After that `main.py` copies titles table from one database to second and result is tested in `test_database_post.py`.

### Solved issues

- Copying execution time

With usage of method `cursor.execute(query)` in loop insertion process took about 60 seconds.

It was a little bit too long, so it was replaced with `cursor.executemany(query, params)` which makes insertion only once - loop is run only for creating list of parameters. This not only reduced execution time to an average of 11 seconds but also caused the next issue. Insertion could not be executed until the following issue was resolved.

- Max allowed packet size

By default `cursor.executemany()` method is not able to transfer big packets in security purposes.
The solution was to add command to both database containers in `docker-compose.yml`:

```yaml
command: --max_allowed_packet=1000000000
```
