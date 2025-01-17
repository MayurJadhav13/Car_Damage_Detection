import cv2  # OpenCV library for image processing
import pandas as pd  # For data handling, though not currently used in this code
from ultralytics import YOLO  # For loading and using YOLO detection model
import streamlit as st  # For creating a web application
import numpy as np  # For handling arrays, e.g., converting image data
from PIL import Image  # For image handling and conversion
import google.generativeai as genai  # For integrating Google Gemini model for image descriptions

# Load the YOLO model with the specified weights file
model = YOLO(r"C:\Users\thatw\OneDrive\Desktop\woxsen\SEM 7\CV\cv project\CarDD_release\CarDD_release\CarDD_COCO\Dataset\runs\detect\train3\weights\best.pt")

# Function to predict detections using the YOLO model
def predict(chosen_model, img, classes=[], conf=0.5):
    # If specific classes are provided, filter detections by those classes
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        # Predict without filtering classes
        results = chosen_model.predict(img, conf=conf)
    return results  # Return prediction results

# Function to detect objects, draw bounding boxes, and annotate detected classes
def predict_and_detect(chosen_model, img, classes=[], conf=0.5):
    img_copy = img.copy()  # Create a copy of the image to avoid modifying the original
    results = predict(chosen_model, img_copy, classes, conf=conf)  # Get detection results
    
    # Iterate over each detection result
    for result in results:
        # Check if any bounding boxes were detected
        if result.boxes is not None:
            for box in result.boxes:
                # Extract coordinates of the bounding box and the detected class ID
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordinates
                cls_id = int(box.cls[0])  # Class ID
                class_name = result.names[cls_id]  # Get class name based on ID
                
                # Draw the bounding box on the image in red and add class name label
                cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Bounding box
                cv2.putText(img_copy, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)  # Label
    return img_copy, results  # Return annotated image and results

# Function to get a description of detected damages from Google Gemini API
def get_gemini_response(input, image):
    # Configure Google Gemini API with API key
    genai.configure(api_key="#replace with your API")
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use specific Gemini model version
    if input != "":
        # Generate a response based on the input prompt and image
        response = model.generate_content([input, image])
    else:
        # Generate response based on the image only if no input prompt is given
        response = model.generate_content(image)
    return response.text  # Return the text description generated by Gemini

# Initialize the Streamlit app with a title and configuration
st.set_page_config(page_title="Car Damage Detection and Description")
st.title("Upload the Image for Detections and Description!")

# Allow users to upload an image file in JPEG or PNG format
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

if uploaded_file is not None:
    # Read the uploaded image from the byte stream
    image_bytes = uploaded_file.getvalue()
    orig_image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Run object detection on the uploaded image
    result_img, results = predict_and_detect(model, orig_image, classes=[], conf=0.5)

    # Display the original image with a caption
    st.subheader("Original Image")
    st.image(orig_image, caption='Original Image', use_column_width=True)

    # Convert the detected image to RGB format for correct display in Streamlit
    st.subheader("Detected Objects")
    result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    st.image(result_img_rgb, caption='Detected Objects', use_column_width=True)

    # Convert the detected image to PIL format for input into Google Gemini model
    pil_image = Image.fromarray(result_img_rgb)

    # Use a prompt to request a description of detected damages from Gemini model
    input_prompt = "Describe the detected damages in the image."
    gemini_response = get_gemini_response(input_prompt, pil_image)

    # Display the descriptive response from Gemini
    st.subheader("Description of Detected Damages")
    st.write(gemini_response)
