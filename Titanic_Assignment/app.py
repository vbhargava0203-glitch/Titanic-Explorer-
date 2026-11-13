"""Launch with: python -m streamlit run app.py"""
from pathlib import Path
import re

import streamlit as st

from db import passenger_query, run_query, validate_query
from quiz import QUESTIONS, score_answers

st.set_page_config(page_title="Titanic Explorer", page_icon="🚢", layout="wide")
st.title("Titanic Explorer")
st.caption("ET Lab Week 11 · PostgreSQL, Python and Streamlit")
page = st.sidebar.radio("Navigation", ["Dashboard", "Data Explorer", "SQL Lab", "Interactive Test"])
st.sidebar.caption("891 passenger records · Original missing values preserved")


def show_database_error(error):
    st.error("Could not load data from PostgreSQL. Check the database setup and connection settings in README.md.")
    with st.expander("Database error"):
        st.code(str(error))


def reset_quiz():
    st.session_state.pop("quiz_result", None)
    for i in range(len(QUESTIONS)):
        st.session_state.pop(f"question_{i}", None)


if page == "Dashboard":
    st.header("Passenger overview")
    try:
        totals = run_query("""
            SELECT COUNT(*) AS total, COALESCE(SUM(survived), 0) AS survivors,
                   ROUND(100.0 * SUM(survived) / NULLIF(COUNT(*), 0), 2) AS survival_pct,
                   ROUND(AVG(age)::numeric, 2) AS avg_age,
                   ROUND(AVG(fare)::numeric, 2) AS avg_fare
            FROM titanic_project.passengers
        """).iloc[0]
        if int(totals["total"]) == 0:
            st.info("The passengers table is empty. Complete the import steps in README.md.")
            st.stop()
        cols = st.columns(4)
        cols[0].metric("Passengers", f"{int(totals['total']):,}")
        cols[1].metric("Survivors", int(totals["survivors"]))
        cols[2].metric("Non-survivors", int(totals["total"] - totals["survivors"]))
        cols[3].metric("Survival rate", f"{float(totals['survival_pct']):.2f}%")
        st.caption(f"Average known age: {float(totals['avg_age']):.2f} years · Average fare: {float(totals['avg_fare']):.2f} dataset fare units")
        by_class = run_query("""
            SELECT pclass::text AS class, SUM(survived) AS survived,
                   COUNT(*) - SUM(survived) AS did_not_survive
            FROM titanic_project.passengers GROUP BY pclass ORDER BY pclass
        """)
        by_sex = run_query("""
            SELECT sex, SUM(survived) AS survived, COUNT(*) - SUM(survived) AS did_not_survive
            FROM titanic_project.passengers GROUP BY sex ORDER BY sex
        """)
        left, right = st.columns(2)
        with left:
            st.subheader("Survival counts by class")
            st.bar_chart(by_class.set_index("class"), color=["#167D8D", "#AEBCC5"])
        with right:
            st.subheader("Survival counts by sex")
            st.bar_chart(by_sex.set_index("sex"), color=["#167D8D", "#AEBCC5"])
        st.subheader("Missing values")
        missing = run_query("""
            SELECT COUNT(*) - COUNT(age) AS missing_age,
                   COUNT(*) - COUNT(embarked) AS missing_embarked,
                   COUNT(*) - COUNT(cabin) AS missing_cabin
            FROM titanic_project.passengers
        """)
        st.dataframe(missing, hide_index=True, use_container_width=True)
        st.caption("NULL values remain unchanged. Average age excludes passengers with unknown age.")
    except Exception as error:
        show_database_error(error)

elif page == "Data Explorer":
    st.header("Explore passenger records")
    with st.form("passenger_filters"):
        left, middle, right = st.columns(3)
        classes = left.multiselect("Passenger class", [1, 2, 3], default=[1, 2, 3])
        sexes = middle.multiselect("Sex", ["female", "male"], default=["female", "male"])
        outcome = right.selectbox("Survival status", ["All", "Survived", "Did not survive"])
        name = st.text_input("Name contains", placeholder="For example: Braund")
        limit = st.slider("Maximum records", min_value=10, max_value=1000, value=100, step=10)
        load = st.form_submit_button("Load Passenger Data", type="primary")
    if load:
        st.session_state.pop("passenger_result", None)
        if not classes or not sexes:
            st.warning("Select at least one passenger class and one sex.")
        else:
            try:
                sql, params = passenger_query(classes, sexes, outcome, name, limit)
                st.session_state["passenger_result"] = run_query(sql, params)
            except Exception as error:
                show_database_error(error)
    if "passenger_result" in st.session_state:
        frame = st.session_state["passenger_result"]
        st.caption(f"{len(frame)} records from the last submitted filters. The maximum-record limit applies.")
        st.dataframe(frame, hide_index=True, use_container_width=True)
        st.download_button("Download displayed records", frame.to_csv(index=False).encode("utf-8"),
                           "titanic_filtered.csv", "text/csv")

elif page == "SQL Lab":
    st.header("Practice SQL")
    st.caption("Run one SELECT or WITH query. Results are limited to 1,000 rows; queries time out after 5 seconds.")
    sql_source = (Path(__file__).parent / "sql" / "05_analysis.sql").read_text(encoding="utf-8")
    blocks = re.split(r"-- Q\d+: ", sql_source)[1:]
    examples = {block.split("\n", 1)[0]: block.split("\n", 1)[1].strip() for block in blocks}
    example = st.selectbox("Example query", list(examples))
    sql_text = st.text_area("SQL query", value=examples[example], height=240, key=f"sql_{example}")
    if st.button("Run SQL Query", type="primary"):
        st.session_state.pop("sql_result", None)
        try:
            valid_sql = validate_query(sql_text)
            st.session_state["sql_result"] = run_query(valid_sql)
            st.success("Query completed.")
        except ValueError as error:
            st.warning(str(error))
        except Exception as error:
            show_database_error(error)
    if "sql_result" in st.session_state:
        frame = st.session_state["sql_result"]
        st.caption(f"Last successful query result: {len(frame)} rows shown.")
        if frame.attrs.get("truncated"):
            st.warning("The result exceeds 1,000 rows. Only the first 1,000 are displayed and exported.")
        st.dataframe(frame, hide_index=True, use_container_width=True)
        st.download_button("Download query result", frame.to_csv(index=False).encode("utf-8"),
                           "sql_query_result.csv", "text/csv")
    with st.expander("Practice tasks"):
        st.markdown("1. Display the first 20 passengers.\n2. Count passengers by class.\n3. Calculate average fare.\n4. Find passengers with missing ages.\n5. Compare survival rates by sex.\n6. Count passengers by embarkation port.\n7. Find the maximum fare in each class.\n8. Compare survivors and non-survivors by class.")

else:
    st.header("PostgreSQL and Streamlit test")
    st.write("Answer all 15 questions, then submit to see your score and explanations.")
    st.button("Retake Test", on_click=reset_quiz)
    with st.form("knowledge_test"):
        answers = []
        for i, (question, options, correct, explanation) in enumerate(QUESTIONS):
            answer = st.radio(f"{i + 1}. {question}", range(len(options)),
                              format_func=lambda j, opts=options: opts[j],
                              index=None, key=f"question_{i}")
            answers.append(answer)
        submitted = st.form_submit_button("Submit Test", type="primary")
    if submitted:
        st.session_state.pop("quiz_result", None)
        try:
            score = score_answers(answers)
            st.session_state["quiz_result"] = {"score": score, "answers": answers.copy()}
        except ValueError as error:
            st.warning(str(error))
    if "quiz_result" in st.session_state:
        result = st.session_state["quiz_result"]
        percentage = result["score"] / len(QUESTIONS) * 100
        left, right = st.columns(2)
        left.metric("Correct answers", f"{result['score']} / {len(QUESTIONS)}")
        right.metric("Percentage", f"{percentage:.2f}%")
        st.progress(percentage / 100)
        st.write("Excellent work!" if percentage >= 80 else "Good effort. Review the explanations." if percentage >= 60 else "Keep practicing and review the explanations.")
        for i, (question, options, correct, explanation) in enumerate(QUESTIONS):
            chosen = result["answers"][i]
            label = "Correct" if chosen == correct else "Incorrect"
            with st.expander(f"Question {i + 1}: {label}"):
                st.write(f"Your answer: {options[chosen]}")
                st.write(f"Correct answer: {options[correct]}")
                st.write(explanation)
        st.caption("Scores are kept for this session only and are not saved to PostgreSQL.")

st.divider()
st.caption("Titanic Dataset Project | Python + Streamlit + PostgreSQL")
