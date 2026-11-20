-- Шаг 1: выполни этот файл в pgAdmin (подключение к postgres / любая системная БД).

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname IN ('ticktick_db') AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS ticktick_db;

DROP ROLE IF EXISTS ticktick_user;

CREATE USER ticktick_user WITH PASSWORD 'ticktick_user';
CREATE DATABASE ticktick_db OWNER ticktick_user;
GRANT ALL PRIVILEGES ON DATABASE ticktick_db TO ticktick_user;

-- Шаг 2: в pgAdmin открой Query Tool на базе ticktick_db и выполни Backend/ticktick_schema.sql
-- Шаг 3: в терминале Backend: alembic upgrade head