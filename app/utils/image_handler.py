import cv2
from io import BytesIO
import numpy as np

def process_image(image_file):
    """
    Process the input image to detect the largest face and draw a bounding box around it.

    Args:
        image_file: A file-like object containing the image data.

    Returns:
        tuple: A tuple containing:
            - bytes: The processed image with the bounding box encoded as JPG.
            - tuple or None: The coordinates (x, y, w, h) of the largest face, or None if no face is detected.
    """
    in_memory_file = BytesIO()  # Creating a temporary in memory storage for the image
    image_file.save(in_memory_file)

    image_bytes = in_memory_file.getvalue()
    nparr = np.frombuffer(image_bytes, np.uint8) # Convert to numpy array

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # Decode image
    
    if img is None:
        return image_bytes, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converting the image to grayscale

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Load face detector

    faces = face_cascade.detectMultiScale(gray, 1.1, 5) # Detect faces

    if len(faces)==0:
        return image_bytes, None

    largest_face = max(faces, key=lambda x: x[2]*x[3]) # Get largest face

    (x, y, w, h) = largest_face

    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3) # Draw box

    is_sucess, buffer = cv2.imencode('.jpg', img) # Encode to JPG

    return buffer.tobytes(), largest_face