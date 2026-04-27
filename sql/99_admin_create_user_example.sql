-- admin_create_user_example.sql
-- Run this manually as the PostgreSQL admin user.
-- Do not put your real password in GitHub.

CREATE ROLE cs623_user
WITH LOGIN
PASSWORD 'replace_with_password'
NOSUPERUSER
NOCREATEDB
NOCREATEROLE;

ALTER DATABASE cs623_project OWNER TO cs623_user;

GRANT CONNECT ON DATABASE cs623_project TO cs623_user;