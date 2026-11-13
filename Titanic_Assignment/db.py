"""PostgreSQL access for the local teaching app. No CSV fallback."""
from contextlib import closing
import os

import pandas as pd
import psycopg2
import sqlparse
from sqlparse import tokens as T


def database_config():
    """Environment variables override the optional Streamlit secrets file."""
    import streamlit as st
    try:
        secrets = dict(st.secrets.get("db", {}))
    except FileNotFoundError:
        secrets = {}
    defaults = {"host": "localhost", "port": 5432, "dbname": "titanic_db", "user": "titanic_app"}
    env_names = {"host": "PGHOST", "port": "PGPORT", "dbname": "PGDATABASE",
                 "user": "PGUSER", "password": "PGPASSWORD", "sslmode": "PGSSLMODE"}
    config = {**defaults, **secrets}
    for key, env_name in env_names.items():
        if os.environ.get(env_name):
            config[key] = os.environ[env_name]
    return config


def run_query(sql, params=None, max_rows=1000):
    """Execute a query in a fresh read-only transaction, closing all resources."""
    with closing(psycopg2.connect(
        **database_config(), connect_timeout=5,
        application_name="titanic_assignment",
        options="-c default_transaction_read_only=on -c statement_timeout=5000 -c lock_timeout=1000",
    )) as connection:
        connection.set_session(readonly=True)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                if cursor.description is None:
                    raise ValueError("The query must return a table.")
                rows = cursor.fetchmany(max_rows + 1)
                frame = pd.DataFrame(rows[:max_rows], columns=[c.name for c in cursor.description])
                frame.attrs["truncated"] = len(rows) > max_rows
                return frame


def validate_query(sql):
    """Friendly single-SELECT validation; permissions remain the real boundary."""
    statements = [s for s in sqlparse.parse(sql) if str(s).strip()]
    if len(statements) != 1 or statements[0].get_type() != "SELECT":
        raise ValueError("Enter one SELECT query, optionally beginning with WITH.")
    for token in statements[0].flatten():
        if token.ttype in T.Keyword.DML and token.normalized != "SELECT":
            raise ValueError("Data-changing statements are not allowed.")
        if token.ttype in T.Keyword.DDL or (token.ttype in T.Keyword and token.normalized in {
            "INTO", "FOR UPDATE", "FOR SHARE", "COPY", "CALL", "SET", "RESET", "GRANT", "REVOKE"
        }):
            raise ValueError("Only read-only queries are allowed.")
    return str(statements[0]).strip()


def passenger_query(classes, sexes, outcome, name, limit):
    sql = """SELECT passengerid, name, sex, age, pclass, fare, embarked,
                    cabin, sibsp, parch, ticket, survived
             FROM titanic_project.passengers
             WHERE pclass = ANY(%s) AND sex = ANY(%s)"""
    params = [classes, sexes]
    if outcome != "All":
        sql += " AND survived = %s"
        params.append(1 if outcome == "Survived" else 0)
    if name.strip():
        # Escape LIKE wildcards so the input is a literal name substring.
        term = name.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        sql += " AND name ILIKE %s"
        params.append("%" + term + "%")
    sql += " ORDER BY passengerid LIMIT %s"
    params.append(int(limit))
    return sql, params
