<<<<<<< HEAD
import torch
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import numpy as np

# Select device (GPU if available, else CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load FaceNet model once (important for performance)
model = InceptionResnetV1(pretrained="vggface2").eval().to(device)


def get_embedding(face_img):
    """
    Convert detected face image into a 512-D face embedding
    """

    # Resize face image
    img = Image.fromarray(face_img).resize((160, 160))

    # Normalize image
    img = np.array(img).astype("float32") / 255.0

    # Convert to tensor
    tensor = torch.tensor(img).permute(2, 0, 1).unsqueeze(0).to(device)

    # Generate embedding
    with torch.no_grad():
        embedding = model(tensor)

=======
import torch
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import numpy as np

# Select device (GPU if available, else CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load FaceNet model once (important for performance)
model = InceptionResnetV1(pretrained="vggface2").eval().to(device)


def get_embedding(face_img):
    """
    Convert detected face image into a 512-D face embedding
    """

    # Resize face image
    img = Image.fromarray(face_img).resize((160, 160))

    # Normalize image
    img = np.array(img).astype("float32") / 255.0

    # Convert to tensor
    tensor = torch.tensor(img).permute(2, 0, 1).unsqueeze(0).to(device)

    # Generate embedding
    with torch.no_grad():
        embedding = model(tensor)

>>>>>>> d7aab021af56edae4ca8a7650116415220551368
    return embedding.cpu().numpy()[0]