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

    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (emp_id,))
    if cursor.fetchone():
        st.error("Employee ID already exists!")
        conn.close()
        return

    st.info("Capture face using camera")

    image = st.camera_input("Take a photo")

    if image is None:
        st.warning("Please capture an image")
        return

    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    face = detect_face(frame)

    if face is None:
        st.error("No face detected")
        return

    embedding = get_embedding(face)

    if embedding is None:
        st.error("Embedding failed")
        return

    mean_embedding = embedding

    registration_date = datetime.date.today()
    registration_time = datetime.datetime.now().strftime("%H:%M:%S")

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
            mean_embedding.tobytes(),
            registration_date,
            registration_time
        )
    )

    conn.commit()
    conn.close()

    st.success("Employee registered successfully")