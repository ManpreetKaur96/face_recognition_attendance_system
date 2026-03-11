import cv2
import numpy as np
import sqlite3
import datetime
import streamlit as st
import time

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

    st.info("📷 Camera starting... Look straight at camera")

    cap = cv2.VideoCapture(0)

    # Check if camera opened
    if not cap.isOpened():
        st.error("Unable to access camera.")
        return

    embeddings = []
    count = 0

    # Give camera time to warm up
    time.sleep(2)

    while count < 15:
        ret, frame = cap.read()

        if not ret:
            continue

        face = detect_face(frame)

        if face is not None:
            embedding = get_embedding(face)

            if embedding is not None:
                embeddings.append(embedding)
                count += 1

                cv2.putText(
                    frame,
                    f"Capturing {count}/15",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                # Small delay between captures
                time.sleep(0.3)

        cv2.imshow("Register Face - Press Q to Cancel", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Validation
    if len(embeddings) < 10:
        st.error("Face not captured properly. Please try again.")
        return

    # Average embedding
    mean_embedding = np.mean(embeddings, axis=0)

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

    st.success("✅ Employee Registered Successfully!")