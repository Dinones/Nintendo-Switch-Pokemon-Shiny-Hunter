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

import sys; sys.path.append('..'); sys.path.append('../Utils') 
import Constants as CONST
import Messages as MSG

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

index = 0
pause = False
# ↓↓ Sort images based on alphanumeric order of filenames
images = [image for image in sorted(os.listdir('../Media/Results')) if image.lower().endswith(('.png', '.jpg', 'jpeg'))]
images.sort(key=lambda x: ''.join(filter(str.isdigit, x)))
print(MSG.IMAGES_SUCCESSFULLY_LOADED.replace('{loaded}/{total}', str(len(images))))
print(MSG.PRESS_BUTTON_TO_ACTION.replace('{button}', 'space').replace('{action}', 'pause the program'))
print(MSG.PRESS_BUTTON_TO_ACTION.replace('{button}', 'A\' or \'D').replace('{action}', 'go back / forward while in pause'))
print(MSG.PRESS_BUTTON_TO_ACTION.replace('{button}', 'Q').replace('{action}', 'stop the program'))

timer = time()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

while True and (index + 1) != len(images):
    if time() - timer >= 0.3:
        if pause: index -= 1
        image = cv2.imread(f'../Media/Results/{images[index]}')
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        cv2.putText(image, f'Count: {index}', CONST.TEXT_PARAMS['position'], cv2.FONT_HERSHEY_SIMPLEX, 
            CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
        cv2.imshow('Lost Shiny Checker', image)

        index += 1
        timer = time()

    # ↓↓ Press 'q' to stop the program
    key = cv2.waitKey(1)
    if key in [ord('q'), ord('Q')]: break
    # ↓↓ Press ' ' (space bar) to pause the program  
    elif key == ord(' '): pause = not pause
    # ↓↓ Press 'a' to view the previous image
    elif pause and key in [ord('a'), ord('A')]: index -= 1    
    # ↓↓ Press 'd' to view the following image
    elif pause and key in [ord('d'), ord('D')]: index += 1    

cv2.destroyAllWindows()