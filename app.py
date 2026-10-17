import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)

# ---------- Custom CSS: Dark Slate & Teal Sidebar + Original Metric Cards ----------
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

# ---------- Optional extra: helper functions ----------
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


# ---------- Sidebar menu (Redesigned Style) ----------
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
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #f1f5f9;">Lab 03 Active</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Optional extra: sidebar quick stats and download ----------
with st.sidebar:
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

# ---------- Original Content Code Below ----------

if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

    # ---------- Optional extra: feature cards and risk overview ----------
    st.subheader("What You Can Do")

    card1, card2, card3 = st.columns(3)

    with card1:
        feature_card("📊", "Dashboard", "Filter students and view metrics and charts.")

    with card2:
        feature_card("🗂️", "Student Data", "Inspect the CSV data and search by name or course.")

    with card3:
        feature_card("🛡️", "Risk Checker", "Check the risk level of one student.")

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
    st.title("Interactive Dashboard")

    st.write("Use the filters below to explore student performance.")

    selected_course = st.selectbox(
        "Select Course",
        ["All"] + list(student_df["Course"].unique())
    )

    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )

    min_attendance = st.slider(
        "Minimum Attendance",
        0,
        100,
        0
    )

    min_score = st.slider(
        "Minimum Score",
        0,
        100,
        0
    )

    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Dataset")
        st.dataframe(filtered_df)

        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if len(filtered_df) > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.warning("No data available for score chart.")

    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            risk_count = filtered_df["Risk Level"].value_counts()
            st.bar_chart(risk_count)
        else:
            st.warning("No data available for risk chart.")

    st.write("Course Count")

    if len(filtered_df) > 0:
        course_count = filtered_df["Course"].value_counts()
        st.bar_chart(course_count)
    else:
        st.warning("No data available for course chart.")

    # ---------- Optional extra: top students and students needing support ----------
    st.subheader("Top 3 Students")

    if len(filtered_df) > 0:
        top_students = filtered_df.nlargest(3, "Score")[["Student Name", "Course", "Score", "Risk Level"]]
        st.dataframe(style_risk_table(top_students))
    else:
        st.warning("No data available for top students.")

    st.subheader("Students Who May Need Support")

    support_df = filtered_df[filtered_df["Risk Level"] == "High Risk"]

    if len(support_df) > 0:
        st.dataframe(style_risk_table(support_df))
    else:
        st.success("No high risk students in this selection.")

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
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

    # ---------- Optional extra: search and filter students ----------
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

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

        # ---------- Optional extra: progress bars and advice ----------
        bar_col1, bar_col2 = st.columns(2)

        with bar_col1:
            st.write(f"Score: {input_score}/100")
            st.progress(int(input_score) / 100)

        with bar_col2:
            st.write(f"Attendance: {input_attendance}%")
            st.progress(int(input_attendance) / 100)

        if risk_result == "Low Risk":
            st.info("Advice: Doing well. Keep up the current study habits.")
        elif risk_result == "Medium Risk":
            st.info("Advice: Some support may help, such as extra practice or a short check-in.")
        else:
            st.info("Advice: Offer support early, such as tutoring or a friendly conversation.")

else:
    st.title("About")
    st.write("This app is part of Lab 03.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Data Loading, Layout, and Frontend Prototype")

    st.info(
        "This frontend prototype loads real data from students.csv "
        "and displays it using Streamlit and Pandas."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )

    # ---------- Optional extra: tools cards and risk rules ----------
    st.subheader("Tools Used")

    tool1, tool2, tool3 = st.columns(3)

    with tool1:
        feature_card("🐍", "Python", "Main programming language.")

    with tool2:
        feature_card("🐼", "Pandas", "Loads and processes students.csv.")

    with tool3:
        feature_card("🎈", "Streamlit", "Builds the interactive pages.")

    st.write("")

    with st.expander("How is the risk level calculated?"):
        st.write("High Risk: score below 60 or attendance below 60.")
        st.write("Medium Risk: score below 75 or attendance below 75.")
        st.write("Low Risk: score and attendance are both 75 or higher.")