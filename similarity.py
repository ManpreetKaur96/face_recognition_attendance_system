<<<<<<< HEAD
import numpy as np

def cosine_similarity(a, b):
=======
import numpy as np

def cosine_similarity(a, b):
>>>>>>> d7aab021af56edae4ca8a7650116415220551368
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))