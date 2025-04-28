import os
import shutil  # For deleting non-empty directories

# Paths to reset
student_details_path = "StudentDetails/studentdetails.csv"
attendance_folder = "Attendance"
training_image_folder = "TrainingImage"

# Reset the student details CSV
if os.path.exists(student_details_path):
    with open(student_details_path, "w") as file:
        file.write("Enrollment,Name\n")  # Write only the headers
    print(f"Reset: {student_details_path} has been cleared and reset to headers.")
else:
    print(f"File not found: {student_details_path}")

# Reset the attendance folder
if os.path.exists(attendance_folder):
    for file_name in os.listdir(attendance_folder):
        file_path = os.path.join(attendance_folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Delete non-empty subdirectories
            print(f"Deleted folder: {file_path}")
    print(f"All files in {attendance_folder} have been deleted.")
else:
    print(f"Folder not found: {attendance_folder}")

# Reset the contents of the TrainingImage folder
if os.path.exists(training_image_folder):
    for item in os.listdir(training_image_folder):
        item_path = os.path.join(training_image_folder, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Delete files
            print(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Delete non-empty subdirectories
            print(f"Deleted folder: {item_path}")
    print(f"All contents of {training_image_folder} have been deleted.")
else:
    print(f"Folder not found: {training_image_folder}")