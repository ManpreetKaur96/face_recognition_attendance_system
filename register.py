import sqlite3
import cv2
import numpy as np
import datetime
import streamlit as st

from detector import detect_face
from embedding import get_embedding


def register_employee(emp_id, name, address, email, dob):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check if employee already exists
    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (emp_id,))
    if cursor.fetchone():
        st.error("Employee ID already exists!")
        conn.close()
        return

    st.info("📷 Capture face using camera")

    # Browser camera input
    image = st.camera_input("Take a photo")

    if image is None:
        st.warning("Please capture an image")
        return

    # Convert image to OpenCV format
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    # Detect face
    face = detect_face(frame)

    if face is None:
        st.error("No face detected. Please try again.")
        return

    # Generate embedding
    embedding = get_embedding(face)

    if embedding is None:
        st.error("Face embedding failed")
        return

    registration_date = datetime.date.today()
    registration_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Insert employee into database
    cursor.execute(
        """
        INSERT INTO employees 
        (employee_id, name, address, email, dob, embedding, registration_date, registration_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            emp_id,
            name,
            address,
            email,
            dob,
            embedding.tobytes(),
            registration_date,
            registration_time
        )
    )

    conn.commit()
    conn.close()

    st.success("✅ Employee registered successfully!")