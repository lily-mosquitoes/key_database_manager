#!/bin/bash

mysql -u $MYSQL_USER -h $MYSQL_HOST -p$MYSQL_PASSWORD -e "DROP DATABASE test_key_database;" &> /dev/null
