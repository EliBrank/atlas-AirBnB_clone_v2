-- create database hbnb_dev_db and user hbnb_dev
-- hbnb_dev given all privileges on hbnb_dev_db, SELECT privilege on performance_schema

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS hbnb_dev@localhost IDENTIFIED BY "hbnb_dev_pwd";
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO hbnb_dev@localhost;
GRANT SELECT ON performance_schema.* TO hbnb_dev@localhost;
