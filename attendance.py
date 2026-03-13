<<<<<<< HEAD
import cv2
import numpy as np
import streamlit as st
from datetime import datetime

from database.db import cursor, conn
from detector import detect_face
from embedding import get_embedding
from similarity import cosine_similarity


def mark_attendance():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        st.error("Camera not opening ❌")
        return False

    cursor.execute("SELECT employee_id, embedding FROM employees")
    data = cursor.fetchall()

    if len(data) == 0:
        st.warning("No registered employees found.")
        return False

    # Convert stored embeddings from BLOB to numpy array
    known = [(d[0], np.frombuffer(d[1], dtype=np.float32)) for d in data]

    stframe = st.empty()
    recognized = False

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            st.error("Failed to read camera")
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
                        st.success(f"✅ Attendance marked for {emp_id}")
                        recognized = True

                    else:
                        st.warning(f"⚠ Attendance already marked for {emp_id}")
                        recognized = True

                    break

        # Show frame in Streamlit
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(rgb, channels="RGB")

        if recognized:
            break

    cap.release()
    cv2.destroyAllWindows()

=======
import cv2
import numpy as np
import streamlit as st
from datetime import datetime

from database.db import cursor, conn
from detector import detect_face
from embedding import get_embedding
from similarity import cosine_similarity


def mark_attendance():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        st.error("Camera not opening ❌")
        return False

    cursor.execute("SELECT employee_id, embedding FROM employees")
    data = cursor.fetchall()

    if len(data) == 0:
        st.warning("No registered employees found.")
        return False

    # Convert stored embeddings from BLOB to numpy array
    known = [(d[0], np.frombuffer(d[1], dtype=np.float32)) for d in data]

    stframe = st.empty()
    recognized = False

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            st.error("Failed to read camera")
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
                        st.success(f"✅ Attendance marked for {emp_id}")
                        recognized = True

                    else:
                        st.warning(f"⚠ Attendance already marked for {emp_id}")
                        recognized = True

                    break

        # Show frame in Streamlit
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(rgb, channels="RGB")

        if recognized:
            break

    cap.release()
    cv2.destroyAllWindows()

>>>>>>> d7aab021af56edae4ca8a7650116415220551368
    return recognized