import streamlit as st
import pandas as pd
import plotly.express as px

# Step 9: Update Page Configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)

# Step 10: Remove the Hard-Coded Student Dataset

# Step 11: Add a CSV Loading Function
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()

# Step 12: Load the Student Data
student_df = load_student_data()

# Step 13: Keep the Risk Level Function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Step 14: Add the Risk Level Column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

# # Step 10: Add the Risk Level Column
# student_df["Risk Level"] = student_df.apply(
#     lambda row: get_risk_level(row["Score"], row["Attendance"]),
#     axis=1
# )

# Calculate summary statistics for the full dataset.
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

# Step 15: Keep Sidebar Navigation from Lab 02
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )

# Step 16: Update the Home Page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

# Step 13: Create the Dashboard Page
elif selected_page == "Dashboard":
    st.title("Interactive Dashboard")

    st.write("Use the filters below to explore student performance.")

    # Step 14: Add Course Filter
    selected_course = st.selectbox(
        "Select Course",
        ["All"] + list(student_df["Course"].unique())
    )

    # Step 15: Add Risk Level Filter
    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )

    # Step 16: Add Minimum Attendance Slider
    min_attendance = st.slider(
        "Minimum Attendance",
        0,
        100,
        0
    )

    # Step 17: Add Minimum Score Slider
    min_score = st.slider(
        "Minimum Score",
        0,
        100,
        0
    )

    # Step 18: Update the Dashboard Page
    filtered_df = pd.read_csv("students.csv")

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

    # Step 19: Add Dashboard Metrics
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

    # Step 20: Add Show or Hide Dataset Checkbox
    show_data = st.checkbox("Show Filtered Dataset", True)

    # Step 21: Add Download Button
    if show_data:
        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")

    # Step 22: Add Student Score Chart
    st.subheader("Charts")

    chart_col1, chart_col2, chart_col3, chart_col4 = st.columns(4)

    with chart_col1:
        st.write("Student Scores")

        if len(filtered_df) > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.warning("No data available for score chart.")

    # Add Risk Level Count Chart
    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            risk_colors = {"Low Risk": "#22c55e", "Medium Risk": "#f59e0b", "High Risk": "#ef4444"}
            risk_count_df = filtered_df["Risk Level"].value_counts().reset_index()
            risk_count_df.columns = ["Risk Level", "Count"]
            fig_risk = px.bar(
                risk_count_df, x="Risk Level", y="Count",
                color="Risk Level", color_discrete_map=risk_colors
            )
            fig_risk.update_layout(showlegend=False, margin=dict(t=10, b=10))
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.warning("No data available for risk chart.")

    # Add Score vs Attendance Scatter Chart
    with chart_col3:
        st.write("Score vs Attendance")

        if len(filtered_df) > 0:
            risk_colors = {"Low Risk": "#22c55e", "Medium Risk": "#f59e0b", "High Risk": "#ef4444"}
            fig_scatter = px.scatter(
                filtered_df, x="Score", y="Attendance",
                color="Risk Level", color_discrete_map=risk_colors,
                hover_name="Student Name"
            )
            fig_scatter.update_layout(margin=dict(t=7, b=7))
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No data available for scatter chart.")

    # Step 23c: Add Study Hours Line Chart
    with chart_col4:
        st.write("Study Hours per Student")

        if len(filtered_df) > 0:
            study_chart = filtered_df.set_index("Student Name")["Study Hours"]
            st.line_chart(study_chart)
        else:
            st.warning("No data available for line chart.")


# Step 24: Update the Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")

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

# Step 25: Create the Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Use this page to check the risk level of one student based on "
        "score and attendance."
    )

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

# Step 26: Update the About Page
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

if st.button("click me"):
    st.write("welcome")
