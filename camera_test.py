"""
Camera test before gathering data
"""

import cv2

cam = cv2.VideoCapture(0)


cv2.namedWindow("test")

img_counter = 0

scale = 10
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    
    #get the webcam size
    height, width, channels = frame.shape

    #prepare the crop
    centerX, centerY = int(height/2), int(width/2)
    radiusX, radiusY = int(scale*height/100), int(scale*width/100)
    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))           
    
    flip_gray = cv2.cvtColor(cv2.flip(resized_cropped,1), cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("test", flip_gray)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, flip_gray)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()