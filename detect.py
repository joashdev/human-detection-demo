# import opencv
import cv2
import imutils
import numpy as np
from imutils.object_detection import non_max_suppression

# use HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# test and test1 are too noisy
vid = cv2.VideoCapture("./test0.mp4")

while vid.isOpened():
  captured, frame = vid.read()

  if captured:
    frame = imutils.resize(frame, width=min(800, frame.shape[1]))

    # detectMultiScale to detect multiple pedestrians in a frame
    (regions, _) = hog.detectMultiScale(frame, winStride=(4,4), padding=(4,4), scale=1.3)
    
    '''
      the following commented codeblock does not use non-max-suppression
      to put the rectangle boundary on detected pedestrian
      resulting to overlaping rectangle boundaries
    '''
    # for (x,y,w,h) in regions:
    #   cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
    
    regions = np.array([[x, y, x + w, y + h] for (x, y, w, h) in regions])
    pick = non_max_suppression(regions, probs=None, overlapThresh=0.65)
    
    # put the rectangle boundary to each pedestrian
    for (xA, yA, xB, yB) in pick:
      cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("Pedestrians", frame)
    if cv2.waitKey(25) == 13:
      break
  else:
    break

vid.release()
cv2.destroyAllWindows()