-- Q01: Total passengers
SELECT COUNT(*) AS total_passengers FROM titanic_project.passengers;

-- Q02: Missing values
SELECT COUNT(*) AS total_records,
       COUNT(age) AS available_age,
       COUNT(*) - COUNT(age) AS missing_age,
       COUNT(*) - COUNT(embarked) AS missing_embarked,
       COUNT(*) - COUNT(cabin) AS missing_cabin
FROM titanic_project.passengers;

-- Q03: Survival distribution
SELECT survived, COUNT(*) AS passengers
FROM titanic_project.passengers GROUP BY survived ORDER BY survived;

-- Q04: Passenger count by sex
SELECT sex, COUNT(*) AS passengers
FROM titanic_project.passengers GROUP BY sex ORDER BY sex;

-- Q05: Passenger count and average age by class
SELECT pclass, COUNT(*) AS passengers, COUNT(age) AS known_ages,
       ROUND(AVG(age)::numeric, 2) AS average_age
FROM titanic_project.passengers GROUP BY pclass ORDER BY pclass;

-- Q06: Survival rate by sex
SELECT sex, COUNT(*) AS passengers, SUM(survived) AS survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_pct
FROM titanic_project.passengers GROUP BY sex ORDER BY sex;

-- Q07: Passengers with missing age
SELECT passengerid, name, sex, pclass
FROM titanic_project.passengers WHERE age IS NULL ORDER BY passengerid;

-- Q08: Missing values by class
SELECT pclass, COUNT(*) - COUNT(age) AS missing_age,
       COUNT(*) - COUNT(cabin) AS missing_cabin,
       COUNT(*) - COUNT(embarked) AS missing_embarked
FROM titanic_project.passengers GROUP BY pclass ORDER BY pclass;

-- Q09: Average fare by class and embarkation port
SELECT pclass, COALESCE(embarked, 'Unknown') AS port,
       COUNT(*) AS passengers, ROUND(AVG(fare)::numeric, 2) AS average_fare
FROM titanic_project.passengers GROUP BY pclass, embarked
ORDER BY pclass, embarked NULLS LAST;

-- Q10: Survival rate by class and sex
SELECT pclass, sex, COUNT(*) AS passengers, SUM(survived) AS survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_pct
FROM titanic_project.passengers GROUP BY pclass, sex ORDER BY pclass, sex;

-- Q11: Age bands including unknown ages
WITH age_groups AS (
    SELECT CASE WHEN age IS NULL THEN 'Unknown'
                WHEN age < 13 THEN 'Child 0 to under 13'
                WHEN age < 20 THEN 'Teen 13 to under 20'
                WHEN age < 60 THEN 'Adult 20 to under 60'
                ELSE 'Older adult 60 and above' END AS age_band,
           CASE WHEN age IS NULL THEN 5 WHEN age < 13 THEN 1
                WHEN age < 20 THEN 2 WHEN age < 60 THEN 3 ELSE 4 END AS band_order,
           survived
    FROM titanic_project.passengers
)
SELECT age_band, COUNT(*) AS passengers, SUM(survived) AS survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_pct
FROM age_groups GROUP BY age_band, band_order ORDER BY band_order;

-- Q12: Ten highest fares; passengerid breaks ties deterministically
SELECT passengerid, name, pclass, fare
FROM titanic_project.passengers ORDER BY fare DESC NULLS LAST, passengerid LIMIT 10;

-- Q13: Case insensitive name search
SELECT passengerid, name, sex, age, pclass
FROM titanic_project.passengers WHERE name ILIKE '%Braund%' ORDER BY passengerid;

-- Q14: Summary statistics
SELECT COUNT(*) AS passengers, SUM(survived) AS survivors,
       COUNT(*) - SUM(survived) AS non_survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_pct,
       ROUND(AVG(age)::numeric, 2) AS average_age,
       ROUND(AVG(fare)::numeric, 2) AS average_fare
FROM titanic_project.passengers;

-- Q15: Survival by class
SELECT pclass, COUNT(*) AS passengers, SUM(survived) AS survivors,
       COUNT(*) - SUM(survived) AS non_survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_pct
FROM titanic_project.passengers GROUP BY pclass ORDER BY pclass;

-- Q16: Embarkation counts; preserve missing port as a separate group
SELECT COALESCE(embarked, 'Unknown') AS port, COUNT(*) AS passengers
FROM titanic_project.passengers GROUP BY embarked ORDER BY embarked NULLS LAST;

-- Q17: Fare statistics by class
SELECT pclass, ROUND(AVG(fare)::numeric, 2) AS average_fare,
       MIN(fare) AS minimum_fare, MAX(fare) AS maximum_fare
FROM titanic_project.passengers GROUP BY pclass ORDER BY pclass;

-- Q18: Subquery example, fares above the dataset average
SELECT COUNT(*) AS passengers_above_average_fare
FROM titanic_project.passengers
WHERE fare > (SELECT AVG(fare) FROM titanic_project.passengers);

-- Q19: First twenty records
SELECT * FROM titanic_project.passengers ORDER BY passengerid LIMIT 20;
