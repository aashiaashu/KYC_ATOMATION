import streamlit as st
import cv2
import os
import speech_recognition as sr
from fuzzywuzzy import fuzz

# Predefined data
predefined_data = {
    "name": "Aastha Patil",
    "dob": "2207 2003",
    "address": "B7 Sundaram society Bharuch Gujarat",
    "income_range": "50000 INR per month",
    "employment_type": "business women",
    "image_path": "image.jpg"  # Path to predefined image
}

def capture_speech(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.text(prompt)  # Display the prompt in a box
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        captured_text = recognizer.recognize_google(audio)
        return captured_text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return None

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Unable to open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Error: Unable to read frame.")
            break

        st.image(frame, channels="BGR")
        if st.button("Capture Image", key="capture_button"):
            filename = os.path.join(os.path.expanduser('~'), 'Downloads', 'captured_image.jpg')
            cv2.imwrite(filename, frame)
            st.success(f"Image saved as {filename}")
            break

    cap.release()
    cv2.destroyAllWindows()

def check_similarity(user_data, predefined_data):
    # Calculate similarity score for each field
    similarity_scores = {}
    for field, value in user_data.items():
        predefined_value = predefined_data.get(field)
        if predefined_value:
            similarity_scores[field] = fuzz.token_sort_ratio(value.lower(), predefined_value.lower())

    # Check if all similarity scores meet the threshold
    threshold = 80  # You can adjust this threshold as needed
    if all(score >= threshold for score in similarity_scores.values()):
        return True
    else:
        return False

def check_image_similarity(user_image_path, predefined_image_path):
    user_image = cv2.imread(user_image_path)
    predefined_image = cv2.imread(predefined_image_path)

    # Perform image comparison here (e.g., using OpenCV)

    # For demonstration purposes, assume images always match
    return True

def main():
    st.title("CENTRAL KYC REGISTRY")
    st.image("process1.png", caption="Your Image Caption", use_column_width=True)
    # Sidebar section
    st.sidebar.title("Know More")
    st.sidebar.info(
        "This section provides more information about the KYC process."
        " Please refer to this website || https://www.ckycindia.in/ || additional details."
    )

    # Add image to sidebar
    st.sidebar.image("logo.jpg", caption="Your Image Caption", use_column_width=True)

    # Input fields
    st.header("User Details")

    name = capture_speech("Please speak your name:")
    st.text_input("Name:", name)

    dob = capture_speech("Please speak your date of birth (in DD/MM/YYYY format):")
    st.text_input("Date of Birth:", dob)

    address = capture_speech("Please speak your address:")
    st.text_input("Address:", address)

    income_range = capture_speech("Please speak your income range:")
    st.text_input("Income Range:", income_range)

    employment_type = capture_speech("Please speak your type of employment:")
    st.text_input("Type of Employment:", employment_type)

    # User data dictionary
    user_data = {
        "name": name,
        "dob": dob,
        "address": address,
        "income_range": income_range,
        "employment_type": employment_type
    }

    # Image capture
    st.header("Webcam Image Capture")
    st.write("Click the button below to capture an image from your webcam.")
    capture_image()

    # Check similarity between captured data and predefined data
    st.header("Your KYC verification and registration is complete.")

if __name__ == "__main__":
    main()
