-- Run after connecting to titanic_db.
BEGIN;
CREATE SCHEMA IF NOT EXISTS titanic_project;;

-- Column order matches the supplied CSV exactly.
CREATE TABLE IF NOT EXISTS titanic_project.titanic_staging (
    name TEXT,
    sex VARCHAR(10),
    age DOUBLE PRECISION,
    sibsp INTEGER,
    parch INTEGER,
    embarked VARCHAR(5),
    ticket TEXT,
    fare DOUBLE PRECISION,
    cabin TEXT,
    passengerid INTEGER,
    pclass INTEGER,
    survived INTEGER
);

CREATE TABLE IF NOT EXISTS titanic_project.passengers (
    passengerid INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    sex VARCHAR(10),
    age DOUBLE PRECISION,
    sibsp INTEGER,
    parch INTEGER,
    embarked VARCHAR(5),
    ticket TEXT,
    fare DOUBLE PRECISION,
    cabin TEXT,
    pclass INTEGER,
    survived INTEGER,
    CONSTRAINT valid_passenger_class CHECK (pclass BETWEEN 1 AND 3),
    CONSTRAINT valid_survival_value CHECK (survived IN (0, 1))
);
COMMIT;
