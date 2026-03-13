import os
import sqlite3
import cv2
import numpy as np
import streamlit as st
from datetime import datetime

from detector import detect_face
from embedding import get_embedding
from similarity import cosine_similarity

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


def mark_attendance():

    cursor.execute("SELECT employee_id, embedding FROM employees")
    data = cursor.fetchall()

    if len(data) == 0:
        st.warning("No employees registered")
        return False

    known = [(d[0], np.frombuffer(d[1], dtype=np.float32)) for d in data]

    # CLOUD MODE
    if os.environ.get("STREAMLIT_SERVER_PORT"):

        image = st.camera_input("Capture face")

        if image is None:
            st.warning("Please capture image")
            return False

        file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        face = detect_face(frame)

        if face is None:
            st.warning("Face not detected")
            return False

        emb = get_embedding(face)

        for emp_id, known_emb in known:

            sim = cosine_similarity(emb, known_emb)

            if sim > 0.75:

                today = datetime.now().strftime('%Y-%m-%d')
                time_now = datetime.now().strftime('%H:%M:%S')

                cursor.execute(
                    "SELECT * FROM attendance WHERE employee_id=? AND date=?",
                    (emp_id, today)
                )

                if not cursor.fetchone():

                    cursor.execute(
                        "INSERT INTO attendance VALUES (NULL,?,?,?)",
                        (emp_id, today, time_now)
                    )

                    conn.commit()
                    st.success(f"Attendance marked for {emp_id}")

                else:
                    st.warning(f"Attendance already marked for {emp_id}")

                return True

        st.error("Face not recognized")
        return False

    # LOCAL MODE
    else:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera not opening")
            return False

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            face = detect_face(frame)

            if face is not None:

                emb = get_embedding(face)

                for emp_id, known_emb in known:

                    sim = cosine_similarity(emb, known_emb)

                    if sim > 0.75:

                        today = datetime.now().strftime('%Y-%m-%d')
                        time_now = datetime.now().strftime('%H:%M:%S')

                        cursor.execute(
                            "SELECT * FROM attendance WHERE employee_id=? AND date=?",
                            (emp_id, today)
                        )

                        if not cursor.fetchone():

                            cursor.execute(
                                "INSERT INTO attendance VALUES (NULL,?,?,?)",
                                (emp_id, today, time_now)
                            )

                            conn.commit()
                            st.success(f"Attendance marked for {emp_id}")

                        else:
                            st.warning(f"Attendance already marked for {emp_id}")

                        cap.release()
                        cv2.destroyAllWindows()

                        return True

            cv2.imshow("Attendance", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return False