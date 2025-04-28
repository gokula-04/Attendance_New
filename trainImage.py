import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow, QLineEdit
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageTk


class Communicate(QObject):
    update_message = pyqtSignal(str)


class FaceRecognizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Recognition Training")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()
        self.communicate = Communicate()
        self.communicate.update_message.connect(self.update_message)

    def initUI(self):
        layout = QVBoxLayout()

        self.message_label = QLabel("Status will appear here", self)
        layout.addWidget(self.message_label)

        self.train_button = QPushButton('Train Image', self)
        self.train_button.clicked.connect(self.train_image)
        layout.addWidget(self.train_button)

        self.setLayout(layout)

    def update_message(self, message):
        self.message_label.setText(message)

    def train_image(self):
        # Call the TrainImage function (passing necessary paths)
        self.TrainImage(
            "haarcascade_frontalface_default.xml",  # Assuming this is the haarcascade file
            "train_images",  # Path to train images directory
            "train_image_labels.yml",  # Path to save trained labels
            self.message_label,
            self.text_to_speech
        )

    def text_to_speech(self, text):
        # Placeholder for text-to-speech functionality
        print(f"Text to Speech: {text}")


def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message_label=None, text_to_speech=None):
    """
    Trains the face recognition model using images in the training directory.
    """
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_cascade = cv2.CascadeClassifier(haarcasecade_path)

        if not os.path.exists(trainimage_path):
            if message_label:
                message_label.setText("Training image directory not found!")
            if text_to_speech:
                text_to_speech("Training image directory not found!")
            return

        image_paths = [os.path.join(trainimage_path, f) for f in os.listdir(trainimage_path)]
        face_samples = []
        ids = []

        for image_path in image_paths:
            pil_image = Image.open(image_path).convert('L')  # Convert to grayscale
            image_np = np.array(pil_image, 'uint8')
            id = int(os.path.split(image_path)[-1].split(".")[1])
            faces = face_cascade.detectMultiScale(image_np)

            for (x, y, w, h) in faces:
                face_samples.append(image_np[y:y + h, x:x + w])
                ids.append(id)

        recognizer.train(face_samples, np.array(ids))
        recognizer.write(trainimagelabel_path)

        if message_label:
            message_label.setText("Model trained successfully!")
        if text_to_speech:
            text_to_speech("Model trained successfully!")

    except Exception as e:
        if message_label:
            message_label.setText(f"Error: {str(e)}")
        if text_to_speech:
            text_to_speech(f"Error: {str(e)}")

    def getImagesAndLables(self, path):
        newdir = [os.path.join(path, d) for d in os.listdir(path)]
        imagePath = [
            os.path.join(newdir[i], f)
            for i in range(len(newdir))
            for f in os.listdir(newdir[i])
        ]
        faces = []
        Ids = []
        for imagePath in imagePath:
            pilImage = Image.open(imagePath).convert("L")
            imageNp = np.array(pilImage, "uint8")
            Id = int(os.path.split(imagePath)[-1].split("_")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = FaceRecognizerApp()
    window.show()
    sys.exit(app.exec_())
