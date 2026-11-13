# Titanic Dataset Assignment

ET Lab Week 11: PostgreSQL, Python and Streamlit.

This project imports the supplied Titanic CSV into PostgreSQL and provides a dashboard, passenger explorer, read-only SQL lab, and 15-question quiz. The app reads PostgreSQL directly. It does not silently substitute CSV data when the database is unavailable.

## Files

- `app.py`, `db.py`, `quiz.py`: application and database code.
- `sql/00_create_database.sql` through `sql/05_analysis.sql`: ordered setup and 19 analysis queries.
- `data/Titanic-Dataset.csv`: unchanged copy of the supplied dataset.
- `results/`: actual query outputs, dataset checks, and verification details.
- `Titanic_Assignment_Report.pdf` and `.md`: printable assignment report and editable Markdown version.
- `.streamlit/secrets.toml.example`: connection settings template with no real password.

## Windows setup

Run commands in PowerShell. Install a standard Windows Python 3.10+ from https://www.python.org/downloads/windows/ and PostgreSQL with its command-line tools if needed. PostgreSQL 17 was present on the computer used to prepare this project. Use your actual installation path if it differs.

1. Extract this entire folder, then open PowerShell **inside the extracted Titanic_Assignment folder**. The import uses a relative path to the included CSV.

2. Create the Python environment and install packages:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `py` reports no installed Python, install or repair standard Windows Python and enable its launcher, or replace `py -3` with the full path to that Python executable. Environment activation is optional because the commands use the environment's Python directly.

3. Set the psql path and create the database. Each command prompts for the administrator password when required:

```powershell
$psql = 'C:\Program Files\PostgreSQL\17\bin\psql.exe'
& $psql -h localhost -U postgres -d postgres -v ON_ERROR_STOP=1 -f sql/00_create_database.sql
& $psql -h localhost -U postgres -d titanic_db -v ON_ERROR_STOP=1 -f sql/01_schema.sql
& $psql -h localhost -U postgres -d titanic_db -v ON_ERROR_STOP=1 -f sql/02_import.psql
& $psql -h localhost -U postgres -d titanic_db -v ON_ERROR_STOP=1 -f sql/03_load_passengers.sql
& $psql -h localhost -U postgres -d titanic_db -v ON_ERROR_STOP=1 -f sql/04_app_role.sql
```

Run these in order, stopping at any error. They are first-time setup scripts. If the database, schema, or role already exists, inspect it before continuing. The import refuses to append to a nonempty staging table, and the primary key prevents duplicate final records. No reset or deletion is performed automatically.

4. Set the app account password interactively:

```powershell
& $psql -h localhost -U postgres -d titanic_db
```

At the `titanic_db=#` prompt, enter:

```text
\password titanic_app
\q
```

5. Copy the configuration template and replace its password with the password you just set:

```powershell
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
notepad .streamlit/secrets.toml
```

The default connection is localhost, port 5432, database `titanic_db`, user `titanic_app`. Keep the real secrets file private. The supplied `.gitignore` excludes it. Alternatively, set `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD` in your environment; these override the secrets file.

6. Verify the records using the app account:

```powershell
& $psql -h localhost -U titanic_app -d titanic_db -c 'SELECT COUNT(*) FROM titanic_project.passengers;'
& $psql -h localhost -U titanic_app -d titanic_db -v ON_ERROR_STOP=1 -f sql/05_analysis.sql
```

The first command must return 891. Expected missing counts: age 177, embarked 2, cabin 687. There are 342 survivors and 549 non-survivors.

7. Start the application:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open http://localhost:8501 in your browser. Press Ctrl+C in the terminal to stop the app.

## Ubuntu lab setup

The assignment PDFs use Ubuntu. The same application and SQL files work there. After installing PostgreSQL, Python, venv support, and pip, open a terminal in the project folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
sudo -u postgres psql -d postgres -v ON_ERROR_STOP=1 -f sql/00_create_database.sql
sudo -u postgres psql -d titanic_db -v ON_ERROR_STOP=1 -f sql/01_schema.sql
sudo -u postgres psql -d titanic_db -v ON_ERROR_STOP=1 -f sql/02_import.psql
sudo -u postgres psql -d titanic_db -v ON_ERROR_STOP=1 -f sql/03_load_passengers.sql
sudo -u postgres psql -d titanic_db -v ON_ERROR_STOP=1 -f sql/04_app_role.sql
sudo -u postgres psql -d titanic_db
```

Use `\password titanic_app` and `\q` inside psql, then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and edit the password. Start with `.venv/bin/python -m streamlit run app.py`. The postgres operating-system account must be able to read this project directory and CSV. If it cannot, connect using a database administrator account with access to the project files rather than weakening permissions on your entire home directory.

## How to demonstrate the project

1. Open Dashboard and show the four headline metrics, charts, and missing-value counts.
2. Open Data Explorer. Choose class 1, female, and survived. Click Load Passenger Data. Export the displayed records.
3. Open SQL Lab and run the survival-by-sex example. Change the SQL and rerun. Only a single SELECT or a WITH query ending in SELECT is accepted.
4. Open Interactive Test. Submit without answers to see validation, answer all questions to see the score, and click Retake Test to clear all answers.
5. Show the database schema and both table counts in psql.

The SQL Lab uses a SELECT-only database role, a read-only transaction, a five-second timeout, and a 1,000-row display/export cap. The query validator is a teaching convenience, not a full security sandbox. This project is configured for local classroom use.

## Before submission

- Fill in your name, roll number, class/section, and submission date on the report cover.
- Read the report and run the application so you can explain it during a demonstration.
- If your instructor separately requires screenshots, capture your own final app and database session after setup. No screenshots are fabricated in this package.
- Submit the report and source files in the format requested by your instructor. Do not include `.venv`, caches, or real database passwords.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Connection refused | Start PostgreSQL and check host/port in the secrets file. |
| Password authentication failed | Check the `titanic_app` password and database username. |
| Relation does not exist | Check database `titanic_db`, schema `titanic_project`, and completion of SQL setup. |
| `\copy` fails in pgAdmin | Run the `.psql` file through the psql command-line client. |
| CSV file not found | Run the import from the project root containing `data/`. |
| Duplicate records or an existing object | Do not rerun setup blindly. Inspect the existing object and resume at the next incomplete step. |
| Module not found | Install requirements with the same `.venv` Python used to start Streamlit. |
| SQL timed out | Simplify the query; the local SQL Lab permits five seconds per statement. |

## Sources

The requirements come from the supplied `ET_lab_week11.pdf` and `ET_LAB_PostgreSQL__Python__and_Streamlit.pdf`. All reported passenger statistics come from the supplied `Titanic-Dataset.csv`, not from an external Titanic dataset.

- PostgreSQL psql and client-side copy: https://www.postgresql.org/docs/17/app-psql.html
- PostgreSQL transaction modes: https://www.postgresql.org/docs/17/sql-set-transaction.html
- Streamlit widget behavior: https://docs.streamlit.io/develop/api-reference/widgets/st.radio
- Streamlit AppTest: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest
