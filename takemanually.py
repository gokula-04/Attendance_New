import sys
import os
import pandas as pd
import datetime
import time
import calendar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

# Initialize Date and Time Variables
ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")
attendance_data = {}
index = 0

# PyQt5 Application for Manually Fill Attendance
class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fill Attendance")
        self.setGeometry(100, 100, 580, 320)

        # Add a gradient background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FFFFFF, stop: 1 #E0E0E0
                );
            }
        """)
        self.initUI()

    def initUI(self):
        # Get the current month name
        current_month = calendar.month_name[datetime.datetime.now().month]

        # Display the current month
        self.subject_label = QLabel(f"Current Month: {current_month}", self)
        self.subject_label.setStyleSheet("""
            QLabel {
                font: bold 15pt;
                color: #000000;  /* Black text */
                background-color: #D6D6D6;  /* Light gray background */
                padding: 10px;
                border-radius: 10px;
            }
        """)

        # "Fill Attendance" button
        self.fill_attendance_button = QPushButton("Fill Attendance", self)
        self.fill_attendance_button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;  /* Light gray */
                color: #000000;            /* Black text */
                font: bold 15pt;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #D6D6D6; /* Slightly darker gray */
            }
        """)
        self.fill_attendance_button.clicked.connect(lambda: self.fill_attendance(current_month))

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.subject_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.fill_attendance_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def fill_attendance(self, subject):
        """
        Fills attendance for the current month.
        """
        try:
            # Read the student details
            student_details_path = "StudentDetails/studentdetails.csv"
            if not os.path.exists(student_details_path):
                QMessageBox.critical(self, "Error", "Student details file not found!")
                return

            df = pd.read_csv(student_details_path)
            if df.empty:
                QMessageBox.warning(self, "Warning", "No student details found!")
                return

            # Process attendance
            attendance_path = f"Attendance/{subject}.csv"
            df["Attendance"] = "Present"
            os.makedirs("Attendance", exist_ok=True)
            df.to_csv(attendance_path, index=False)

            QMessageBox.information(self, "Success", f"Attendance saved for the month: {subject}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


# Global variable to hold the AttendanceApp instance
attendance_window = None

def subjectChoose(text_to_speech=None):
    """
    Launches the AttendanceApp for manually filling attendance.
    Optionally accepts a text-to-speech function.
    """
    global attendance_window  # Use a global variable to persist the window instance

    # Check if a QApplication instance already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Create a new QApplication if none exists

    # Create and show the AttendanceApp window
    if attendance_window is None:  # Only create a new window if one doesn't already exist
        attendance_window = AttendanceApp()  # Store the instance in a global variable
    if text_to_speech:
        text_to_speech("Launching Manual Attendance Application")
    attendance_window.show()

    # Do not call exec_() if the event loop is already running
    if not app.thread().isRunning():
        app.exec_()