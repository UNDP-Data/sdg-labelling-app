# This script inserts test data into a MongoDB container upon start-up
mongoimport --db labelling --collection texts --file /docker-entrypoint-initdb.d/texts.json --jsonArray
mongoimport --db labelling --collection sdgs_users --file /docker-entrypoint-initdb.d/user.json
