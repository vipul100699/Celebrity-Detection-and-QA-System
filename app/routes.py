"""
This module defines the main routes for the application.
It handles the index page, image uploads for celebrity detection, and Q&A interactions.
"""
from flask import Blueprint, render_template, request
from app.utils.qa_engine import QAEngine
from app.utils.celebrity_detector import CelebrityDetector
from app.utils.image_handler import process_image
import base64

# Create a Blueprint for the main application routes
main = Blueprint("main", __name__)

# Initialize the CelebrityDetector and QAEngine instances
celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()

@main.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main page requests.
    
    GET: Renders the initial index page.
    POST: Handles two types of form submissions:
          1. Image Upload: Processes the uploaded image to detect a celebrity.
          2. Question: Processes a user's question about the identified celebrity.
    
    Returns:
        Rendered HTML template with celebrity info, image data, and Q&A results.
    """
    # Initialize variables to store data for the template
    celeb_name = ""
    celeb_info = ""
    result_img_data = ""
    user_question = ""
    answer = ""

    if request.method == "POST":
        # Check if the POST request involves an image upload
        if "image" in request.files:
            image_file = request.files["image"]

            if image_file:
                # Process the image to get bytes and face bounding box
                img_bytes, face_box = process_image(image_file)
                
                # Identify the celebrity in the image
                celeb_info, celeb_name = celebrity_detector.identity(img_bytes)
                print(f"DEBUG: celeb_name: {celeb_name}")
                print(f"DEBUG: celeb_info:\n{celeb_info}")

                # If a face is detected, encode the image for display
                if face_box is not None:
                    result_img_data = base64.b64encode(img_bytes).decode()
                else:
                    celeb_info = "No face detected! Please try another image."

        # Check if the POST request involves a question about the celebrity
        elif "question" in request.form:
            user_question = request.form["question"]

            # Retrieve context data (name, info, image) from hidden form fields
            celeb_name = request.form["celeb_name"]
            celeb_info = request.form["celeb_info"]
            result_img_data = request.form["result_img_data"]

            # Use the QA engine to get an answer to the user's question
            answer = qa_engine.ask_about_celebrity(celeb_name, user_question)

    # Render the index template with all the collected information
    return render_template(
        "index.html",
        celeb_info=celeb_info,
        result_img_data=result_img_data,
        user_question=user_question,
        answer=answer
    )
