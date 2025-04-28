import csv
import os
import cv2
import numpy as np

def TakeImage(enrollment_no, name, haarcascade_path, trainimage_path, message_label, text_to_speech):
    """
    Captures images of the user and saves them in the specified directory.

    Args:
        enrollment_no (str): Enrollment number of the student.
        name (str): Name of the student.
        haarcascade_path (str): Path to the Haarcascade XML file.
        trainimage_path (str): Path to save the training images.
        message_label (QLabel): Label to display messages in the UI.
        text_to_speech (function): Function to convert text to speech.
    """
    if not enrollment_no and not name:
        message = "Please enter both Enrollment Number and Name."
        text_to_speech(message)
        message_label.setText(message)
        return
    if not enrollment_no:
        message = "Please enter your Enrollment Number."
        text_to_speech(message)
        message_label.setText(message)
        return
    if not name:
        message = "Please enter your Name."
        text_to_speech(message)
        message_label.setText(message)
        return

    try:
        # Initialize camera and face detector
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcascade_path)
        sample_num = 0
        directory = f"{enrollment_no}_{name}"
        path = os.path.join(trainimage_path, directory)

        # Ensure directories exist
        os.makedirs(trainimage_path, exist_ok=True)
        if os.path.exists(path):
            message = "Student data already exists."
            text_to_speech(message)
            message_label.setText(message)
            return
        os.mkdir(path)

        # Capture images
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sample_num += 1
                img_path = os.path.join(path, f"{name}_{enrollment_no}_{sample_num}.jpg")
                cv2.imwrite(img_path, gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imshow("Frame", img)

            if cv2.waitKey(1) & 0xFF == ord("q") or sample_num >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        # Save student details
        os.makedirs("StudentDetails", exist_ok=True)
        with open("StudentDetails/studentdetails.csv", "a+", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([enrollment_no, name])

        message = f"Images saved for Enrollment No: {enrollment_no}, Name: {name}."
        text_to_speech(message)
        message_label.setText(message)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        text_to_speech(error_message)
        message_label.setText(error_message)