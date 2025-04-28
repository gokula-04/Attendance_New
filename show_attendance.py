import pandas as pd
from glob import glob
import os
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
import sys

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.text()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        filenames = glob(
            f"Attendance\\{Subject}\\{Subject}*.csv"
        )
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'

        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        # Create new window to display the attendance
        attendance_window = QWidget()
        attendance_window.setWindowTitle(f"Attendance of {Subject}")
        attendance_window.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        cs = f"Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            table = QTableWidget()
            table.setRowCount(len(list(reader)))
            table.setColumnCount(len(next(csv.reader(file))))

            file.seek(0)  # Reset the file reader
            for r, row in enumerate(reader):
                for c, row_data in enumerate(row):
                    table.setItem(r, c, QTableWidgetItem(row_data))

        layout.addWidget(table)
        attendance_window.setLayout(layout)
        attendance_window.show()

    app = QApplication(sys.argv)
    subject_window = QWidget()
    subject_window.setWindowTitle("Subject...")
    subject_window.setGeometry(100, 100, 580, 320)

    layout = QVBoxLayout()

    titl = QLabel("Which Subject of Attendance?")
    titl.setStyleSheet("background-color: black; color: green; font-size: 25px;")
    layout.addWidget(titl)

    tx = QLineEdit()
    tx.setPlaceholderText("Enter Subject")
    tx.setStyleSheet("background-color: black; color: yellow; font-size: 30px; padding: 10px;")
    layout.addWidget(tx)

    def open_subject_folder():
        sub = tx.text()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    check_sheets_btn = QPushButton("Check Sheets")
    check_sheets_btn.setStyleSheet("background-color: black; color: yellow; font-size: 15px; padding: 10px;")
    check_sheets_btn.clicked.connect(open_subject_folder)
    layout.addWidget(check_sheets_btn)

    view_attendance_btn = QPushButton("View Attendance")
    view_attendance_btn.setStyleSheet("background-color: black; color: yellow; font-size: 15px; padding: 10px;")
    view_attendance_btn.clicked.connect(calculate_attendance)
    layout.addWidget(view_attendance_btn)

    subject_window.setLayout(layout)
    subject_window.show()

    sys.exit(app.exec_())
