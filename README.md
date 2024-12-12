# Car Damage Detection and Description

This project detects and describes car damages from uploaded images using a YOLO model for object detection and Google Gemini for generating descriptions. The project uses Streamlit to create a web-based interface for uploading images, detecting damages, and displaying descriptive responses.

## Features

- YOLO Detection: Identifies car damages (like dents, scratches) in uploaded images.
- Google Gemini Integration: Generates detailed descriptions of detected damages.
- Streamlit Web App: User-friendly interface for uploading and viewing results.

## Prerequisites

- Python 3.8 or higher
- A Google Gemini API key for the image description feature.

## Setup

### 1. Install the dependencies

From the project directory, install the necessary libraries:

```bash
pip install -r requirements.txt

2. Set up the Google Gemini API Key

 - To use the Google Gemini model, you need an API key:
 - Obtain an API key from Google Cloud Platform.
 - Set up the API key as an environment variable:
    - export GOOGLE_API_KEY="your-google-api-key"
3. Model Weights
 - Place the YOLO model weights (best.pt) in the specified path as per your code:
   C:\Users\thatw\OneDrive\Desktop\woxsen\SEM 7\CV\cv project\CarDD_release\CarDD_release\CarDD_COCO\Dataset\runs\detect\train3\weights\best.pt

Running the Application

 - Start the Streamlit app with the following command:
    streamlit run app.py

 - This will launch a local server where you can interact with the app.

Usage
 - Open the app in your browser (usually http://localhost:8501).
 - Upload a car image to analyze.
 - View the detected damages and generated descriptions in the app