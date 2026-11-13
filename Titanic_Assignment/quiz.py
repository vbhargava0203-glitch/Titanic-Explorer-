"""Fifteen questions covering the concepts in the supplied lab guides."""
QUESTIONS = [
    ("What is a database used for?", ["Storing and managing data", "Designing slides", "Compiling Python", "Replacing an OS"], 0, "A database organizes stored information for retrieval and management."),
    ("What is a PostgreSQL schema?", ["A CSV file", "A namespace for database objects", "A password", "A Python package"], 1, "Schemas organize tables and other objects inside a database."),
    ("Which command creates a schema?", ["MAKE SCHEMA", "NEW SCHEMA", "CREATE SCHEMA", "INSERT SCHEMA"], 2, "CREATE SCHEMA creates a namespace within the current database."),
    (r"What does psql \copy do?", ["Deletes records", "Imports or exports through the client", "Creates a user", "Changes a password"], 1, r"\copy reads or writes a file using the psql client's filesystem access."),
    ("What does HEADER TRUE mean during CSV import?", ["The first row contains column names", "All columns are required", "Every column is a key", "The last row is skipped"], 0, "The first CSV row is skipped because it contains the header."),
    ("How many passenger records are in this dataset?", ["714", "889", "891", "204"], 2, "The supplied CSV contains 891 data rows."),
    ("How many age values are missing?", ["177", "204", "687", "2"], 0, "891 rows minus 714 known ages equals 177 missing ages."),
    ("What does a primary key enforce?", ["Identical values", "Unique and non-NULL key values", "Text-only values", "No missing ages"], 1, "The primary key uniquely identifies each passenger and cannot be NULL."),
    ("Which expression counts all rows?", ["TOTAL()", "NUMBER()", "COUNT(*)", "ROWS()"], 2, "COUNT(*) includes all rows, regardless of NULLs in individual columns."),
    ("What does GROUP BY do?", ["Forms groups for aggregate calculations", "Deletes duplicates", "Imports CSV", "Creates tables"], 0, "Rows sharing grouping values are aggregated together."),
    ("Which SQL command retrieves records?", ["SHOW ROWS", "SELECT", "DISPLAY", "FETCH TABLE"], 1, "SELECT retrieves data and computed expressions."),
    ("What is Streamlit used for?", ["Building interactive Python web apps", "Replacing PostgreSQL", "Creating every table automatically", "Replacing Python"], 0, "Streamlit turns Python code into an interactive web interface."),
    ("Which library connects this app to PostgreSQL?", ["matplotlib", "psycopg2", "turtle", "random"], 1, "psycopg2 is the PostgreSQL database adapter used by db.py."),
    ("What does COUNT(age) count?", ["All rows", "Only missing ages", "Non-NULL age values", "Only zero ages"], 2, "COUNT(column) ignores NULL values; AVG(column) also excludes NULLs."),
    ("What does survived = 1 mean?", ["The passenger survived", "The passenger did not survive", "Age is unknown", "First class"], 0, "The survival indicator uses 1 for survived and 0 for did not survive."),
]


def score_answers(answers):
    if len(answers) != len(QUESTIONS) or any(answer is None for answer in answers):
        raise ValueError("Answer all 15 questions before submitting.")
    return sum(answer == question[2] for answer, question in zip(answers, QUESTIONS))
