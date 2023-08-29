###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

from time import sleep, time
import cv2

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

index = 0
images = [image for image in sorted(os.listdir('../Media/Results'), key=lambda x: int(x.split('.')[0]))]
timer = time()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

while True and (index + 1) != len(images):
    if time() - timer >= 0.3:
        image = cv2.imread(f'../Media/Results/{images[index]}')
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        cv2.putText(image, f'Count: {index}', CONST.TEXT_PARAMS['position'], cv2.FONT_HERSHEY_SIMPLEX, 
            CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
        cv2.imshow('Lost Shiny Checker', image)

        index += 1
        timer = time()

    # ↓↓ Press 'q' to stop the program
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'): break
    elif key == ord(' '): 

cv2.destroyAllWindows()