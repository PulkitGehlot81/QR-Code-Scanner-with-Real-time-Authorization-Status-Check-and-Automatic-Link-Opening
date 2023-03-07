import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import webbrowser

cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open('./authorized_people.txt') as f:
    authorized_people = f.read().splitlines()

scan_once = True
while True:
    success, img = cap.read()

    try:
        barcodes = decode(img)
    except Exception:
        barcodes = []

    for barcode in barcodes:
        decoded_data = barcode.data.decode('utf-8')
        print(decoded_data)

        if decoded_data.startswith('http'):
            webbrowser.open(decoded_data)
            authorization_status = 'Link opened'
            outline_color = (255, 0, 0)
        elif decoded_data in authorized_people:
            authorization_status = 'Authorized'
            outline_color = (0, 255, 0)
        else:
            authorization_status = 'Un-Authorized'
            outline_color = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(img, [pts], True, outline_color, 5)
        pts2 = barcode.rect
        cv.putText(img, authorization_status, (pts2[0], pts2[1]), cv.FONT_HERSHEY_SIMPLEX,
                    0.9, outline_color, 2)

        scan_once = False

    cv.imshow('Result', img)

    # Check for 'q' key pressed to quit
    if cv.waitKey(1) == ord('q'):
        break

    # Scan the QR code only once
    if not scan_once:
        break

cap.release()
cv.destroyAllWindows()
