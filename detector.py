<<<<<<< HEAD
import torch
from facenet_pytorch import MTCNN
import cv2

# Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize MTCNN face detector
mtcnn = MTCNN(
    keep_all=False,  # Only allow one face
    device=device
)


def detect_face(frame, return_box=False):
    """
    Detect a face from a frame and return the cropped face image.
    Optionally return the bounding box.
    """

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    boxes, probs = mtcnn.detect(rgb_frame)

    # ❌ No face OR multiple faces detected
    if boxes is None or len(boxes) != 1:
        if return_box:
            return None
        return None

    x1, y1, x2, y2 = boxes[0].astype(int)

    # Safety check to avoid cropping outside frame
    h, w, _ = rgb_frame.shape

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    face_img = rgb_frame[y1:y2, x1:x2]

    if return_box:
        return face_img, (x1, y1, x2, y2)

=======
import torch
from facenet_pytorch import MTCNN
import cv2

# Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize MTCNN face detector
mtcnn = MTCNN(
    keep_all=False,  # Only allow one face
    device=device
)


def detect_face(frame, return_box=False):
    """
    Detect a face from a frame and return the cropped face image.
    Optionally return the bounding box.
    """

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    boxes, probs = mtcnn.detect(rgb_frame)

    # ❌ No face OR multiple faces detected
    if boxes is None or len(boxes) != 1:
        if return_box:
            return None
        return None

    x1, y1, x2, y2 = boxes[0].astype(int)

    # Safety check to avoid cropping outside frame
    h, w, _ = rgb_frame.shape

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    face_img = rgb_frame[y1:y2, x1:x2]

    if return_box:
        return face_img, (x1, y1, x2, y2)

>>>>>>> d7aab021af56edae4ca8a7650116415220551368
    return face_img