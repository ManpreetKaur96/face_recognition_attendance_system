import os
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

    embeddings = []

    # ---------------- CLOUD MODE ----------------
    if os.environ.get("STREAMLIT_SERVER_PORT"):

        image = st.camera_input("Capture Face")

        if image is None:
            st.warning("Please capture an image")
            return

        file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        face = detect_face(frame)

        if face is None:
            st.error("Face not detected")
            return

        embedding = get_embedding(face)

        if embedding is None:
            st.error("Embedding generation failed")
            return

        embeddings = [embedding] * 15   # simulate multiple captures


    # ---------------- LOCAL MODE ----------------
    else:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Unable to access camera.")
            return

        count = 0

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

                    time.sleep(0.3)

            cv2.imshow("Register Face - Press Q to Cancel", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if len(embeddings) < 10:
            st.error("Face not captured properly. Please try again.")
            return

    # ---------------- SAVE TO DATABASE ----------------

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

    st.success("✅ Employee Registered Successfully!")v