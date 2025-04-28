import sys
import cv2
import os
import time
import datetime
import pandas as pd
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import shutil

# Paths
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "Attendance"


class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subject Attendance")
        self.setGeometry(100, 100, 580, 320)
        self.setStyleSheet("background-color: black; color: yellow;")

        self.subject_label = QLabel("Enter the Subject Name")
        self.subject_label.setFont(QFont("Arial", 25))
        self.subject_label.setAlignment(Qt.AlignCenter)

        self.subject_input = QLineEdit(self)
        self.subject_input.setFont(QFont("Arial", 30))
        self.subject_input.setStyleSheet("background-color: black; color: yellow;")

        self.fill_button = QPushButton("Fill Attendance", self)
        self.fill_button.setFont(QFont("Times New Roman", 15))
        self.fill_button.setStyleSheet("background-color: black; color: yellow;")
        self.fill_button.clicked.connect(self.fill_attendance)

        self.check_button = QPushButton("Check Sheets", self)
        self.check_button.setFont(QFont("Times New Roman", 15))
        self.check_button.setStyleSheet("background-color: black; color: yellow;")
        self.check_button.clicked.connect(self.check_sheets)

        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Times New Roman", 15, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.fill_button)
        layout.addWidget(self.check_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def fill_attendance(self):
        sub = self.subject_input.text()
        if sub == "":
            self.status_label.setText("Please enter the subject name!!!")
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            if not os.path.exists(trainimagelabel_path):
                self.status_label.setText("Model not found, please train the model")
                return
            recognizer.read(trainimagelabel_path)

            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            if not os.path.exists(haarcasecade_path):
                self.status_label.setText("Haarcascade file not found!")
                return

            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                self.status_label.setText("Unable to access the camera!")
                return

            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            now = time.time()
            future = now + 20

            while time.time() < future:
                ret, im = cam.read()
                if not ret:
                    self.status_label.setText("Failed to capture frame from camera!")
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    enrollment_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                    if confidence < 70:
                        student_name = df.loc[df["Enrollment"] == enrollment_id, "Name"].values
                        if len(student_name) > 0:
                            student_name = student_name[0]
                            attendance.loc[len(attendance)] = [enrollment_id, student_name]
                            label = f"{enrollment_id} - {student_name}"
                        else:
                            label = "Unknown"
                    else:
                        label = "Unknown"

                    color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)
                    cv2.rectangle(im, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(im, label, (x, y - 10), font, 0.8, color, 2)

                cv2.imshow("Filling Attendance...", im)
                if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
                    break

            if not attendance.empty:
                attendance.drop_duplicates(subset=["Enrollment"], inplace=True)
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                timestamp = datetime.datetime.now().strftime("%H-%M-%S")
                subject_path = os.path.join(attendance_path, sub)
                os.makedirs(subject_path, exist_ok=True)
                file_path = os.path.join(subject_path, f"{sub}_{date}_{timestamp}.csv")
                attendance.to_csv(file_path, index=False)
                self.status_label.setText(f"Attendance saved successfully for {sub}!")
            else:
                self.status_label.setText("No attendance recorded!")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
        finally:
            cam.release()
            cv2.destroyAllWindows()

    def check_sheets(self):
        sub = self.subject_input.text()
        if sub == "":
            self.status_label.setText("Please enter the subject name!!!")
            return
        try:
            path = os.path.join(attendance_path, sub)
            if not os.path.exists(path):
                self.status_label.setText("No attendance sheets found for this subject!")
                return
            os.startfile(path)
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")


def subjectChoose(text_to_speech=None):
    """
    Launches the AttendanceApp for marking attendance.
    Optionally accepts a text-to-speech function.
    """
    # Check if a QApplication instance already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)  # Create a new QApplication if none exists

    window = AttendanceApp()
    if text_to_speech:
        text_to_speech("Launching Attendance Application")
    window.show()

    # Only call exec_() if QApplication is newly created
    if app is None:
        sys.exit(QApplication.exec_())

if __name__ == "__main__":
    subjectChoose()