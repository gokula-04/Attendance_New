import sys
import os
from typing import Any
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap
import pyttsx3
import pandas as pd
from datetime import datetime

# Project module imports
import show_attendance
import takeImage
import trainImage
import automaticAttedance
import takemanually  # Ensure takemanually is imported

class FaceRecognizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognizer")
        self.setGeometry(100, 100, 1280, 720)

        # Add a gradient background without borders
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FFFFFF, stop: 1 #E0E0E0
                );
            }
        """)

        # Define paths
        self.haarcasecade_path = "haarcascade_frontalface_default.xml"
        self.trainimage_path = "./TrainingImage"
        self.trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"

        # Ensure required folders exist
        os.makedirs(self.trainimage_path, exist_ok=True)
        os.makedirs(os.path.dirname(self.trainimagelabel_path), exist_ok=True)

        # Get the current month dynamically
        self.current_month = datetime.now().strftime("%B")  # e.g., "April"

        self.initUI()

    def initUI(self):
        # Main vertical layout with padding
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around the layout

        # Add animated text at the top
        self.animated_text_label = QLabel(f"For {self.current_month}", self)
        self.animated_text_label.setStyleSheet("color: #000000; font-size: 20px; font-weight: bold;")
        self.animated_text_label.setAlignment(Qt.AlignCenter)  # Align the text to the center
        main_layout.addWidget(self.animated_text_label, alignment=Qt.AlignTop)
        self.start_text_animation()

        # Add space between animated text and other elements
        main_layout.addSpacing(20)

        # Government Emblem and Ministry Information
        emblem_label = QLabel("Government Of India", self)
        emblem_label.setStyleSheet("color: #000000; font-size: 20px; font-weight: bold;")  # Black text
        main_layout.addWidget(emblem_label, alignment=Qt.AlignCenter)

        ministry_label = QLabel("Ministry of Digital Affairs", self)
        ministry_label.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold;")  # Black text
        main_layout.addWidget(ministry_label, alignment=Qt.AlignCenter)

        # Logo at the top
        logo_label = QLabel(self)
        logo_path = "UI_Image/tn.png"
        if os.path.exists(logo_path):
            logo = QPixmap(logo_path).scaled(150, 150, Qt.KeepAspectRatio)
            logo_label.setPixmap(logo)
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Add space between logo and title
        main_layout.addSpacing(20)  # Add 20px of vertical space

        # Title below the logo
        title_label = QLabel("Automated Death Verification System", self)
        title_label.setStyleSheet("""
            color: #000000;  /* Black text */
            font-size: 28px; 
            font-weight: bold; 
            margin-bottom: 20px;
        """)
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Spacer to push buttons to the center of the screen
        main_layout.addStretch()

        # Buttons in the center
        button_layout = QHBoxLayout()

        # Left-side buttons
        left_button_layout = QVBoxLayout()
        left_button_layout.setSpacing(30)  # Add more space between buttons

        register_button = QPushButton("New Registration", self)
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;  /* Light gray */
                color: #000000;            /* Black text */
                font-size: 16px; 
                font-weight: bold; 
                border-radius: 15px;       /* Rounded corners */
                padding: 10px 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            }
            QPushButton:hover {
                background-color: #D6D6D6; /* Slightly darker gray */
            }
        """)
        register_button.clicked.connect(self.takeImageUI)
        left_button_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        attendance_button = QPushButton("Take Certification", self)
        attendance_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;  /* Light gray */
                color: #000000;            /* Black text */
                font-size: 16px; 
                font-weight: bold; 
                border-radius: 15px;       /* Rounded corners */
                padding: 10px 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            }
            QPushButton:hover {
                background-color: #D6D6D6; /* Slightly darker gray */
            }
        """)
        attendance_button.clicked.connect(self.take_certification)
        left_button_layout.addWidget(attendance_button, alignment=Qt.AlignCenter)

        # Right-side buttons
        right_button_layout = QVBoxLayout()
        right_button_layout.setSpacing(30)  # Add more space between buttons

        view_button = QPushButton("View Certification", self)
        view_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;  /* Light gray */
                color: #000000;            /* Black text */
                font-size: 16px; 
                font-weight: bold; 
                border-radius: 15px;       /* Rounded corners */
                padding: 10px 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            }
            QPushButton:hover {
                background-color: #D6D6D6; /* Slightly darker gray */
            }
        """)
        view_button.clicked.connect(self.view_attendance)
        right_button_layout.addWidget(view_button, alignment=Qt.AlignCenter)

        exit_button = QPushButton("Exit", self)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;  /* Light gray */
                color: #000000;            /* Black text */
                font-size: 16px; 
                font-weight: bold; 
                border-radius: 15px;       /* Rounded corners */
                padding: 10px 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            }
            QPushButton:hover {
                background-color: #D6D6D6; /* Slightly darker gray */
            }
        """)
        exit_button.clicked.connect(self.close)
        right_button_layout.addWidget(exit_button, alignment=Qt.AlignCenter)

        # Add left and right button layouts to the horizontal layout
        button_layout.addLayout(left_button_layout)
        button_layout.addLayout(right_button_layout)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Spacer to push buttons to the center of the screen
        main_layout.addStretch()

        # Digital India Initiative
        initiative_label = QLabel("Digital India Initiative", self)
        initiative_label.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold;")  # Black text
        main_layout.addWidget(initiative_label, alignment=Qt.AlignCenter)

        # Set the main layout for the window
        self.setLayout(main_layout)

    def start_text_animation(self):
        """
        Starts the animation for the text "For [Month]".
        """
        self.text_position = self.width()  # Start from the right edge of the window
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_text)
        self.timer.start(30)  # Update every 30ms

    def animate_text(self):
        """
        Moves the text "For [Month]" from right to left.
        """
        self.text_position -= 5  # Move 5 pixels to the left
        if self.text_position < -200:  # Reset position when it goes off-screen
            self.text_position = self.width()
        self.animated_text_label.move(self.text_position, 20)  # Update the label's position (aligned at the top)

    def text_to_speech(self, text):
        """
        Converts the given text to speech using pyttsx3.
        """
        try:
            if not hasattr(self, 'engine'):
                self.engine = pyttsx3.init()  # Initialize the pyttsx3 engine only once

            self.engine.stop()  # Stop any ongoing speech synthesis
            self.engine.say(text)
            self.engine.runAndWait()  # Run the event loop for the current speech
        except RuntimeError as e:
            print(f"Error in text-to-speech: {e}")

    def takeImageUI(self):
        self.ImageUI = QWidget()
        self.ImageUI.setWindowTitle("Take Student Image")
        self.ImageUI.setGeometry(100, 100, 780, 480)
        self.ImageUI.setStyleSheet("background-color: #3B4252;")

        layout = QVBoxLayout()

        title_label = QLabel("Register Your Face", self.ImageUI)
        title_label.setStyleSheet("color: #A3BE8C; font-size: 30px; font-weight: bold;")
        layout.addWidget(title_label)

        self.enrollment_input = QLineEdit(self.ImageUI)
        self.enrollment_input.setPlaceholderText("Enter Enrollment No")
        self.enrollment_input.setStyleSheet("""
            background-color: #4C566A; 
            color: #ECEFF4; 
            font-size: 16px; 
            padding: 5px;
        """)
        layout.addWidget(self.enrollment_input)

        self.name_input = QLineEdit(self.ImageUI)
        self.name_input.setPlaceholderText("Enter Name")
        self.name_input.setStyleSheet("""
            background-color: #4C566A; 
            color: #ECEFF4; 
            font-size: 16px; 
            padding: 5px;
        """)
        layout.addWidget(self.name_input)

        self.message_label = QLabel("", self.ImageUI)
        self.message_label.setStyleSheet("color: #ECEFF4; font-size: 14px;")
        layout.addWidget(self.message_label)

        take_image_button = QPushButton("Take Image", self.ImageUI)
        take_image_button.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                border-radius: 10px; 
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        take_image_button.clicked.connect(self.take_image)
        layout.addWidget(take_image_button)

        train_image_button = QPushButton("Train Image", self.ImageUI)
        train_image_button.setStyleSheet("""
            QPushButton {
                background-color: #A3BE8C; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                border-radius: 10px; 
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #B5D19C;
            }
        """)
        train_image_button.clicked.connect(self.train_image)
        layout.addWidget(train_image_button)

        self.ImageUI.setLayout(layout)
        self.ImageUI.show()

    def take_image(self):
        enrollment_no = self.enrollment_input.text()
        name = self.name_input.text()
        if not enrollment_no or not name:
            self.message_label.setText("Enrollment & Name required!")
            return
        takeImage.TakeImage(enrollment_no, name, self.haarcasecade_path, self.trainimage_path, self.message_label, self.text_to_speech)
        self.enrollment_input.clear()
        self.name_input.clear()

    def train_image(self):
        trainImage.TrainImage(self.haarcasecade_path, self.trainimage_path, self.trainimagelabel_path, self.message_label, self.text_to_speech)

    def automatic_attendance(self):
        automaticAttedance.subjectChoose(self.text_to_speech)

    def view_attendance(self):
        """
        Displays the attendance data in a new window with styled table.
        """
        # Path to the attendance file
        attendance_file = "Attendance/April.csv"  # Replace with the actual file path

        # Check if the file exists
        if not os.path.exists(attendance_file):
            self.text_to_speech("Attendance file not found!")
            print("Error: Attendance file not found!")
            return

        # Read the attendance data
        try:
            df = pd.read_csv(attendance_file)
        except Exception as e:
            self.text_to_speech("Error reading attendance file!")
            print(f"Error reading attendance file: {e}")
            return

        # Create a new dialog to display the attendance
        dialog = QDialog(self)
        dialog.setWindowTitle("View Certification")
        dialog.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Add a title
        title_label = QLabel("Attendance Data", dialog)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #88C0D0; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Create a table to display the data
        table = QTableWidget(dialog)
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        # Populate the table with data
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)  # Center-align text
                table.setItem(i, j, item)

        # Style the table
        table.setStyleSheet("""
            QTableWidget {
                background-color: #ECEFF4;
                alternate-background-color: #D8DEE9;
                gridline-color: #4C566A;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #5E81AC;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #4C566A;
            }
        """)
        table.setAlternatingRowColors(True)  # Enable alternating row colors
        table.horizontalHeader().setStretchLastSection(True)  # Stretch the last column
        table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # Center-align headers

        layout.addWidget(table)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def take_certification(self):
        """
        Trigger the manual attendance application.
        """
        print("Take Certification triggered")
        takemanually.subjectChoose(self.text_to_speech)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceRecognizerApp()
    window.show()
    sys.exit(app.exec_())