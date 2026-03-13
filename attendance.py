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

    # Load known embeddings
    known = [(d[0], np.frombuffer(d[1], dtype=np.float32)) for d in data]

    st.info("📷 Capture face for attendance")

    # Browser camera input
    image = st.camera_input("Take a photo for attendance")

    if image is None:
        st.warning("Please capture a photo")
        return False

    # Convert image to OpenCV format
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    # Detect face
    face = detect_face(frame)

    if face is None:
        st.warning("Face not detected")
        return False

    # Generate embedding
    emb = get_embedding(face)

    if emb is None:
        st.error("Face embedding failed")
        return False

    # Compare with known embeddings
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
                st.success(f"✅ Attendance marked for {emp_id}")

            else:
                st.warning(f"⚠ Attendance already marked for {emp_id}")

            return True

    st.error("❌ Face not recognized")
    return False