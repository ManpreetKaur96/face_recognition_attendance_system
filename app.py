import streamlit as st
import sqlite3
import pandas as pd
import datetime
import db

from register import register_employee
from attendance import mark_attendance

# ---------------- DATABASE VIEW FUNCTIONS ----------------

def view_employees():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("""
        SELECT employee_id, name, address, email, dob, 
               registration_date, registration_time 
        FROM employees
    """, conn)
    conn.close()
    return df

def view_attendance():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM attendance", conn)
    conn.close()
    return df

# ---------------- APP TITLE ----------------

st.title("Face Recognition Attendance System")

option = st.sidebar.selectbox(
    "Select Option",
    ("Register Employee", "Mark Attendance", "View Employees", "View Attendance", "Manage Employees")
)

# ---------------- REGISTER SECTION ----------------
if option == "Register Employee":
    st.subheader("Register New Employee")

    emp_id = st.text_input("Employee ID")
    name = st.text_input("Name")
    address = st.text_input("Address")
    email = st.text_input("Email")
    dob = st.date_input(
        "Date of Birth",
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date.today(),
        value=datetime.date(2000, 1, 1)
    )

    if st.button("Start Face Registration"):

        if emp_id and name and address and email and dob:

            register_employee(
                emp_id,
                name,
                address,
                email,
                str(dob)
            )

        else:
            st.warning("Please fill all fields")

# ---------------- ATTENDANCE SECTION ----------------
elif option == "Mark Attendance":
    st.subheader("Mark Attendance")

    if st.button("Start Attendance"):
        result = mark_attendance()

        if result:
            st.success("Attendance Marked Successfully ✅")
        else:
            st.warning("No Face Detected or Already Marked Today")

# ---------------- VIEW EMPLOYEES ----------------

elif option == "View Employees":
    st.subheader("Registered Employees")
    st.dataframe(view_employees(), use_container_width=True)

# ---------------- VIEW ATTENDANCE ----------------


elif option == "View Attendance":
    st.subheader("Attendance Records")
    st.dataframe(view_attendance(), use_container_width=True)

# ---------------- MANAGE EMPLOYEES ----------------

elif option == "Manage Employees":
    st.subheader("Update or Delete Employee")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT employee_id, name FROM employees")
    employees = cursor.fetchall()

    emp_ids = [emp[0] for emp in employees]

    selected_id = st.selectbox("Select Employee ID", emp_ids)

    cursor.execute("SELECT name, address, email, dob FROM employees WHERE employee_id=?", (selected_id,))
    emp = cursor.fetchone()

    name = st.text_input("Name", emp[0])
    address = st.text_input("Address", emp[1])
    email = st.text_input("Email", emp[2])
    dob = st.text_input("DOB", emp[3])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Update Employee"):
            cursor.execute(
                "UPDATE employees SET name=?, address=?, email=?, dob=? WHERE employee_id=?",
                (name, address, email, dob, selected_id)
            )
            conn.commit()
            st.success("Employee Updated Successfully")

    with col2:
        if st.button("Delete Employee"):
            cursor.execute("DELETE FROM employees WHERE employee_id=?", (selected_id,))
            conn.commit()
            st.warning("Employee Deleted Successfully")

    conn.close()