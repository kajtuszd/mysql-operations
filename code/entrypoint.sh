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

# chmod +x wait-for-it.sh
# ./wait-for-it.sh -t 80 mysql1:3306 || exit 1

# ./wait-for-it.sh -t 80 mysql2:3306 || exit 1

echo '______________________'
echo '______________________'
echo '______________________'
python main.py
