-- Atomic transfer. Running again fails on the primary key and rolls back.
BEGIN;
INSERT INTO titanic_project.passengers (
    passengerid, name, sex, age, sibsp, parch, embarked,
    ticket, fare, cabin, pclass, survived
)
SELECT passengerid, name, sex, age, sibsp, parch, embarked,
       ticket, fare, cabin, pclass, survived
FROM titanic_project.titanic_staging;

DO $$
BEGIN
    IF (SELECT COUNT(*) FROM titanic_project.passengers) <> 891 THEN
        RAISE EXCEPTION 'Expected 891 final records. Transfer rolled back.';
    END IF;
END $$;
COMMIT;
