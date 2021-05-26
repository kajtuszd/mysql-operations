#!/bin/bash

until nc -z -v -w30 mysql1 3306
do
  echo "Waiting for first database connection..."
  sleep 5
done

until nc -z -v -w30 mysql2 3306
do
  echo "Waiting for second database connection..."
  sleep 5
done

pytest test_database_pre.py
echo '____________________________________'
python main.py
echo '____________________________________'
pytest test_database_post.py
