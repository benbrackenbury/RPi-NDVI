import numpy as np
import cv2
from filters import Filters

# This will return video from the first webcam on your computer.
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# loop runs if capturing has been initialized.
while(True):
  # reads frames from a camera
  # ret checks return at each frame
  ret, frame = cap.read()

  # Converts to HSV color space, OCV reads colors as BGR
  # frame is converted to hsv
  contrasted = Filters.contrast_stretch(frame)
  
  # output the frame
  out.write(frame)
  
  # The original input frame is shown in the window
  cv2.imshow('Original', frame)

  # The window showing the operated video stream
  cv2.imshow('frame', contrasted)

  
  # Wait for 'a' key to stop the program
  if cv2.waitKey(1) & 0xFF == ord('a'):
    break

# Close the window / Release webcam
cap.release()

# After we release our webcam, we also release the output
out.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()
