###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import cv2

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MAX_DEVICE_ANALIZER = 10

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

print('\n[♦️] Capture devices found:')
# ↓↓ Print the index of all available capture devices
for index in range(MAX_DEVICE_ANALIZER):
    video_capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if video_capture.read()[0]: print(f"    Video Capture {index}: OK")
    else: print(f"    Video Capture {index}: NOT OK")
    video_capture.release()
print('\n[♦️] Note: The video capture 0 is usually the computer webcam\n')