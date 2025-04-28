import requests
import cv2
import numpy as np
import time

url = "http://192.168.0.6:8080/shot.jpg"

while True:
    try:
        # Send GET request to retrieve the image
        cam = requests.get(url, timeout=2)  # Added timeout to prevent hanging
        if cam.status_code == 200:  # Check if the request was successful
            imgNp = np.array(bytearray(cam.content), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            
            if img is not None:
                cv2.imshow("cam", img)
            else:
                print("Error: Unable to decode image")
        
        else:
            print(f"Error: Failed to retrieve image, Status Code: {cam.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    # Wait for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # To avoid overloading the server, introduce a small delay
    time.sleep(0.1)

cv2.destroyAllWindows()
