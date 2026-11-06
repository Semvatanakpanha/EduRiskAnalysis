import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
    page_icon="🎓",
    layout="wide"
)

# ---------- Custom CSS: dark slate and teal sidebar, metric cards ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Sidebar Background: Modern Deep Slate / Charcoal */
    [data-testid="stSidebar"] {
        background-color: #0b1120 !important;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Original Metric Cards */
    [data-testid="stMetric"] {
        background-color: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 12px;
        padding: 14px 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        # students.csv has an unnamed index column; hide it from every table
        data = data.loc[:, ~data.columns.str.startswith("Unnamed")]
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


student_df = load_student_data()

def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

# ---------- Session state: temporary risk-check history (used by Risk Checker) ----------
# Temporary memory for recent risk checks (lost when the browser session ends).
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

if "history_cleared" not in st.session_state:
    st.session_state["history_cleared"] = False


def clear_risk_history():
    """Callback for the Clear History button (runs BEFORE the page redraws)."""
    st.session_state["risk_history"] = []
    st.session_state["history_cleared"] = True


# ---------- Helper functions ----------
def style_risk_table(df):
    """Color the Risk Level column: green, orange, red."""
    risk_styles = {
        "Low Risk": "color: #22c55e; font-weight: 600;",
        "Medium Risk": "color: #f59e0b; font-weight: 600;",
        "High Risk": "color: #ef4444; font-weight: 600;",
    }

    def color_risk(column):
        return [risk_styles.get(value, "") for value in column]

    return df.style.apply(color_risk, subset=["Risk Level"])


def feature_card(icon, title, text):
    """Small rounded card used on the Home and About pages."""
    st.markdown(
        f"""
        <div style="background-color: rgba(20, 184, 166, 0.08); border: 1px solid rgba(20, 184, 166, 0.35);
                    border-radius: 12px; padding: 16px 18px; height: 100%;">
            <div style="font-size: 26px;">{icon}</div>
            <div style="font-size: 16px; font-weight: 600; margin-top: 6px;">{title}</div>
            <div style="font-size: 14px; opacity: 0.75; margin-top: 4px;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- Sidebar: brand, menu, workspace, quick stats ----------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #1e293b; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 20px;">🎓</span>
                <span style="font-size: 18px; font-weight: 700; color: #f8fafc; letter-spacing: -0.02em;">EduRisk Portal</span>
            </div>
            <p style="margin: 4px 0 0 0; font-size: 12px; color: #64748b;">Academic Performance Hub</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Dashboard", "Student Data", "Risk Checker", "About"],
        icons=["house-door", "grid", "card-checklist", "shield-exclamation", "info-circle"],
        default_index=0,
        key="main_menu",
        styles={
            "container": {
                "padding": "0px",
                "background-color": "transparent"
            },
            "icon": {
                "color": "#64748b",
                "font-size": "16px"
            },
            "nav-link": {
                "font-size": "14px",
                "font-weight": "500",
                "color": "#94a3b8",
                "text-align": "left",
                "margin": "6px 0px",
                "padding": "10px 14px",
                "border-radius": "8px",
                "border": "1px solid transparent",
                "--hover-color": "#1e293b"
            },
            "nav-link-selected": {
                "background-color": "#0f766e",
                "color": "#ffffff",
                "font-weight": "600",
                "border": "1px solid #14b8a6"
            },
        }
    )

    st.markdown(
        """
        <div style="margin-top: 30px; padding: 12px; border-radius: 8px; background-color: #1e293b; border: 1px solid #334155;">
            <p style="margin: 0; font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Workspace</p>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #f1f5f9;">Lab 05 Active</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick stats and report download
    sidebar_total = len(student_df)
    sidebar_avg_score = round(student_df["Score"].mean(), 1)
    sidebar_high_risk = student_df[student_df["Risk Level"] == "High Risk"].shape[0]

    st.markdown(
        f"""
        <div style="margin-top: 14px; padding: 12px; border-radius: 8px; background-color: #1e293b; border: 1px solid #334155;">
            <p style="margin: 0 0 8px 0; font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Quick Stats</p>
            <p style="margin: 0; font-size: 13px; color: #f1f5f9;">👥 Students: <b>{sidebar_total}</b></p>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #f1f5f9;">📈 Avg Score: <b>{sidebar_avg_score}</b></p>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #f1f5f9;">🔴 High Risk: <b>{sidebar_high_risk}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.download_button(
        label="⬇️ Download Risk Report",
        data=student_df.to_csv(index=False),
        file_name="student_risk_report.csv",
        mime="text/csv"
    )

# ---------- Pages ----------

if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write("Welcome to Lab 05.")
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

    # feature cards and risk overview
    st.subheader("What You Can Do")

    card1, card2, card3 = st.columns(3)

    with card1:
        feature_card("📊", "Dashboard", "Filter students, view summaries, and explore Plotly charts.")

    with card2:
        feature_card("🗂️", "Student Data", "Inspect the CSV data and search by name or course.")

    with card3:
        feature_card("🛡️", "Risk Checker", "Check one student with a validated form and keep a history.")

    st.write("")
    st.subheader("Risk Overview")

    risk_counts = student_df["Risk Level"].value_counts()

    overview1, overview2, overview3 = st.columns(3)

    with overview1:
        st.metric("🟢 Low Risk", int(risk_counts.get("Low Risk", 0)))

    with overview2:
        st.metric("🟡 Medium Risk", int(risk_counts.get("Medium Risk", 0)))

    with overview3:
        st.metric("🔴 High Risk", int(risk_counts.get("High Risk", 0)))

elif selected_page == "Dashboard":
    st.title("Interactive Student Performance Dashboard")

    st.write(
        "Use filters to explore student performance by course, risk level, "
        "and attendance. The dashboard updates based on your selections."
    )

    # Filters
    st.subheader("Dashboard Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        course_options = ["All"] + sorted(student_df["Course"].unique())
        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )

    with filter_col2:
        risk_options = ["All"] + sorted(student_df["Risk Level"].unique())
        selected_risk = st.selectbox(
            "Filter by Risk Level",
            risk_options
        )

    with filter_col3:
        minimum_attendance = st.slider(
            "Minimum Attendance",
            0,
            100,
            0
        )

    # Apply filters: every metric, table, and chart below uses filtered_df
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= minimum_attendance
    ]

    if filtered_df.empty:
        st.warning("No students match the selected filters. Please adjust the filters.")

    # Filtered metrics
    st.subheader("Filtered Dashboard Metrics")

    filtered_total_students = len(filtered_df)

    if filtered_total_students > 0:
        filtered_average_score = filtered_df["Score"].mean()
        filtered_average_attendance = filtered_df["Attendance"].mean()
        filtered_high_risk_students = filtered_df[
            filtered_df["Risk Level"] == "High Risk"
        ].shape[0]
    else:
        filtered_average_score = 0
        filtered_average_attendance = 0
        filtered_high_risk_students = 0

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Students", filtered_total_students)

    with metric_col2:
        st.metric("Average Score", round(filtered_average_score, 2))

    with metric_col3:
        st.metric(
            "Average Attendance",
            f"{round(filtered_average_attendance, 2)}%"
        )

    with metric_col4:
        st.metric("High Risk", filtered_high_risk_students)

    # Grouped summary tables
    st.subheader("Course Summary")

    if filtered_total_students > 0:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean")
        ).reset_index()

        st.dataframe(course_summary)
    else:
        st.info("No course summary available for the selected filters.")

    st.subheader("Risk Level Summary")

    if filtered_total_students > 0:
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()
        risk_summary.columns = ["Risk Level", "Students"]

        st.dataframe(risk_summary)
    else:
        st.info("No risk summary available for the selected filters.")

    # Streamlit charts
    st.subheader("Streamlit Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if filtered_total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.info("No score chart available.")

    with chart_col2:
        st.write("Students by Course")

        if filtered_total_students > 0:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count)
        else:
            st.info("No course count chart available.")

    # Plotly interactive charts
    st.subheader("Interactive Plotly Charts")

    plotly_col1, plotly_col2 = st.columns(2)

    with plotly_col1:
        st.write("Risk Level Distribution")

        if filtered_total_students > 0:
            risk_summary_chart = filtered_df["Risk Level"].value_counts().reset_index()
            risk_summary_chart.columns = ["Risk Level", "Students"]

            fig_risk = px.bar(
                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_risk, width="stretch")
        else:
            st.info("No risk distribution chart available.")

    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if filtered_total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_score, width="stretch")
        else:
            st.info("No score chart available.")

    # Filtered records
    st.subheader("Filtered Student Records")

    if filtered_total_students > 0:
        st.dataframe(style_risk_table(filtered_df))
    else:
        st.info("No student records to display.")

    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )

elif selected_page == "Student Data":
    st.title("Student Data")

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk Students", high_risk_students)

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

    # search and filter students
    st.subheader("Search Students")

    search_col1, search_col2 = st.columns(2)

    with search_col1:
        search_name = st.text_input("Search by student name", key="search_name")

    with search_col2:
        search_course = st.selectbox(
            "Filter by course",
            ["All"] + list(student_df["Course"].unique()),
            key="search_course"
        )

    search_result = student_df.copy()

    if search_name:
        search_result = search_result[
            search_result["Student Name"].str.contains(search_name, case=False)
        ]

    if search_course != "All":
        search_result = search_result[search_result["Course"] == search_course]

    if len(search_result) > 0:
        st.write(f"Found {len(search_result)} student(s).")
        st.dataframe(style_risk_table(search_result))

        st.download_button(
            label="Download Search Result",
            data=search_result.to_csv(index=False),
            file_name="search_result.csv",
            mime="text/csv"
        )
    else:
        st.warning("No student found.")

elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )

    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )

    # Form: nothing runs until "Check Risk" is clicked
    # Nothing is processed until the submit button is clicked.
    # Score and Attendance are limited to 0-100 by st.number_input itself.
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

    # Validation, risk calculation, and feedback
    if submitted:
        clean_name = input_name.strip()

        if clean_name == "":
            st.warning("Please enter the student name.")
        elif not any(char.isalpha() for char in clean_name):
            st.warning("Student name must contain at least one letter.")
        else:
            risk_result = get_risk_level(input_score, input_attendance)

            result = {
                "Student Name": clean_name,
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }

            st.session_state["risk_history"].append(result)
            st.session_state["history_cleared"] = False

            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")

            st.write("Student Name:", clean_name)
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)

            # Progress bars
            bar_col1, bar_col2 = st.columns(2)

            with bar_col1:
                st.write(f"Score: {input_score}/100")
                st.progress(int(input_score) / 100)

            with bar_col2:
                st.write(f"Attendance: {input_attendance}%")
                st.progress(int(input_attendance) / 100)

    # Recent risk checks (stored in session state)
    st.subheader("Recent Risk Checks")

    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(st.session_state["risk_history"])

        st.dataframe(style_risk_table(history_df))

        st.button("Clear History", on_click=clear_risk_history)
    else:
        if st.session_state["history_cleared"]:
            st.success("Risk check history cleared.")
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

else:
    st.title("About")
    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")

    st.info(
        "This version improves the Dashboard page using grouped summaries, "
        "interactive filters, Streamlit charts, and Plotly charts."
    )

    st.warning(
        "Ethics Reminder: Student performance visualizations should be used responsibly "
        "to support learning and student success."
    )

    # tools cards and risk rules
    st.subheader("Tools Used")

    tool1, tool2, tool3, tool4 = st.columns(4)

    with tool1:
        feature_card("🐍", "Python", "Main programming language.")

    with tool2:
        feature_card("🐼", "Pandas", "Loads and processes students.csv.")

    with tool3:
        feature_card("🎈", "Streamlit", "Builds the interactive pages.")

    with tool4:
        feature_card("📈", "Plotly", "Draws interactive charts.")

    st.write("")

    with st.expander("How is the risk level calculated?"):
        st.write("High Risk: score below 60 or attendance below 60.")
        st.write("Medium Risk: score below 75 or attendance below 75.")
        st.write("Low Risk: score and attendance are both 75 or higher.")