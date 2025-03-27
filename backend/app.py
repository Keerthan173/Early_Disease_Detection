from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Define upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load AI model (if available)
MODEL_PATH = "model/early_disease_detection_model.h5"
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
else:
    model = None  # Placeholder for when model is missing
    print("⚠️ Model not found! Upload endpoint will work, but predictions won't.")

# Function to preprocess the image
def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))  # Resize to match model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Expand dims to match batch format
    img_array /= 255.0  # Normalize pixel values
    return img_array

# API to upload and process images
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded image
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process image (even if model is not available)
    img_array = prepare_image(file_path)

    # If model is available, make a prediction
    if model:
        prediction = model.predict(img_array)[0][0]
        result = "PNEUMONIA Detected" if prediction > 0.5 else "NORMAL"
    else:
        result = "Model not available, but image uploaded successfully."

    return jsonify({"prediction": result, "file_saved": file_path})

@app.route("/")
def home():
    return "Backend is running! Use /upload to send images."

if __name__ == "__main__":
    app.run(debug=True)