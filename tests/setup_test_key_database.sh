#!/bin/bash

mysql -u $MYSQL_USER -h $MYSQL_HOST -p$MYSQL_PASSWORD < test_key_database.sql #&> /dev/null
