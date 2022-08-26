import numpy as np
import cv2 

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img = cv2.blur(frame, (5, 5))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    scale = 1
    delta = 0
    ddepth = cv2.CV_16S

    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    ret, thresh = cv2.threshold(grad, 10, 255, cv2.THRESH_BINARY_INV)

    c, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    areas = [cv2.contourArea(c1) for c1 in c]
    maxAreaIndex = areas.index(max(areas))

    ct = cv2.drawContours(frame, c, maxAreaIndex, (255, 0, 0), -1)

    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('t', thresh)
    # cv2.imshow('tc', ct)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()