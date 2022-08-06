import cv2
import cvzone
import numpy as np

from functions.drawing_functions import draw as dr
from functions.key_functions import key_sys
from FX1AI_MAIN import FX1AI_MAIN, lcl_var as AI_VAR

import sys
import os
import time

# Initialize Object Detection
os.system("")

VideoSource = "../videos/MV1.mp4"
warning = "sounds/warning.mp3"
cap = cv2.VideoCapture(VideoSource)

VideoSource = VideoSource.replace('../videos/', '')
VideoSource = VideoSource.replace('.mp4', '')

img_logo = dr.make_logo()

hf, wf, cf = img_logo.shape

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 200  # Set Duration To 1000 ms == 1 second

width_f = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height_f = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

hb = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

NEW_SIZE_FACTOR = 0.7
OBJ_DIM = (15, 30)  # heigh, width
CROSSHAIR_DIM = (15, 15)

RED = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (255, 255, 0)
ORANGE = (0, 235, 255)

font = cv2.FONT_HERSHEY_SIMPLEX

# set_line_mode, set_lock_mode, aim_mode, lock_control, ti_proto
ctrl_keys = [0, 0, 1, 0, 0]
proximity = 1;

alpha = 0.4

NUM_PARTICLES = 250
PARTICLE_SIGMA = np.min([OBJ_DIM]) // 4  # particle filter shift per generation
DISTRIBUTION_SIGMA = 0.5

# Initialize count
count = 0
starting_time = time.time()
center_points_prev_frame = []

tracking_objects = {}
track_id = 0
lock_range = 70
lock_range_circle = 23

ret, frame = cap.read()
if not ret:
    sys.exit(0)

img_color = cv2.resize(frame, (int(frame.shape[1] * NEW_SIZE_FACTOR), int(frame.shape[0] * NEW_SIZE_FACTOR)))
img_h, img_w, _ = img_color.shape

# frame center
center_y, center_x = frame.shape[0] // 2, frame.shape[1] // 2

top_left_x = img_w // 2 - OBJ_DIM[1] // 2
top_left_y = img_h // 2 - OBJ_DIM[0] // 2
bot_right_x = img_w // 2 + OBJ_DIM[1] // 2
bot_right_y = img_h // 2 + OBJ_DIM[0] // 2

while True:
    ret, frame = cap.read()
    # Use Only Gray Scale Mode
    # ---->
    # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # <----
    count += 1
    if not ret:
        break
    if ret:
        key = cv2.waitKey(1)

    # Call Key Func !!DONT TOUCH SYSTEM KEY NUMBERS!!
    key_call = key_sys.sys_def_keys(key, ctrl_keys[0], ctrl_keys[1], ctrl_keys[2], ctrl_keys[3], ctrl_keys[4])
    if key_call != None:
        if key_call[0] == 0: ctrl_keys[0] = key_call[1]
        if key_call[0] == 1: ctrl_keys[1] = key_call[1]
        if key_call[0] == 2: ctrl_keys[2] = key_call[1]
        if key_call[0] == 3: ctrl_keys[3] = key_call[1]
        if key_call[0] == 4: ctrl_keys[4] = key_call[1]

    # frame = cv2.normalize(frame, frame, 0, 200, cv2.NORM_MINMAX)

    # anlık frame işaretle
    in_range = False
    in_lock = False
    center_y, center_x = frame.shape[0] // 2, frame.shape[1] // 2
    center_points_cur_frame = []

    # OBJECT DETECTION - CALL FX1 AI----->
    FX1AI = FX1AI_MAIN(frame, width_f, height_f, proximity, ctrl_keys,
                       CYAN, BLACK, ORANGE, WHITE, GREEN, RED,
                       font, center_points_cur_frame,
                       center_x, center_y, in_range, in_lock, track_id, count)
    FX1AI()
    # <-----

    # move_sim area
    dr.make_move_sim_circle(frame, CYAN, font)
    dr.draw_text_w_r(frame, 'F.A.L.S. INIT', 97, 164, CYAN, CYAN, 1, font)

    frame = cv2.putText(frame, 'LINEAR TRACKING:', (20, 85), font, 0.4, CYAN, 1, cv2.LINE_AA)

    if (ctrl_keys[0] == True):
        frame = cv2.putText(frame, 'ONLINE', (136, 85), font, 0.4, GREEN, 1, cv2.LINE_AA)
    else:
        frame = cv2.putText(frame, 'OFFLINE', (136, 85), font, 0.4, CYAN, 1, cv2.LINE_AA)
    # -----
    frame = cv2.putText(frame, 'R-LOCK TRACKING:', (20, 105), font, 0.4, CYAN, 1, cv2.LINE_AA)
    if (ctrl_keys[1] == True):
        frame = cv2.putText(frame, 'ONLINE', (146, 105), font, 0.4, GREEN, 1, cv2.LINE_AA)
    else:
        frame = cv2.putText(frame, 'OFFLINE', (146, 105), font, 0.4, CYAN, 1, cv2.LINE_AA)
    # -----
    frame = cv2.putText(frame, 'AIM MODE:', (20, 135), font, 0.4, CYAN, 1, cv2.LINE_AA)
    if (ctrl_keys[2] == 1):
        frame = cv2.putText(frame, 'PRO', (90, 135), font, 0.4, CYAN, 1, cv2.LINE_AA)
    else:
        frame = cv2.putText(frame, 'SIMPLE', (90, 135), font, 0.4, CYAN, 1, cv2.LINE_AA)

    if (ctrl_keys[1] == False and ctrl_keys[0] == False):

        if (count % 10) == 5:
            # frame = cv2.putText(frame, 'ALERT NO POSITION', (make_text_center(frame, 'ALERT NO POSITION', 0.4,1), center_y+80), font, 0.4, RED,1 ,cv2.LINE_AA)
            space = 1
            # winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
        else:
            frame = cv2.putText(frame, 'WARNING AUTO LOCK SYSTEMS OFFLINE', (
                dr.make_text_center(frame, 'WARNING AUTO LOCK SYSTEMS OFFLINE', 0.4, 1, font), center_y + 110), font,
                                0.4,
                                ORANGE, 1, cv2.LINE_AA)
            # cv2.rectangle(frame, (center_x-50, center_y-50), (center_x+50, center_y+50), (255, 255, 0), 1)

            # frame = cv2.putText(frame, ('PLEASE CHECK WARNINGS'), (center_x+(int(width_f)//2)-(make_text_size(frame, ('PLEASE CHECK WARNINGS'), 0.4)+20), center_y-(int(height_f)//2)+175), font, 0.4, ORANGE,1 ,cv2.LINE_AA)
            dr.draw_text_w_r(frame, 'PLEASE CHECK WARNINGS', int((center_x + (int(width_f) // 2) - (
                    dr.make_text_size(frame, ('PLEASE CHECK WARNINGS'), 0.4, font) + 20))),
                             int((center_y - (int(height_f) // 2) + 195)), BLACK, ORANGE, -1, font)

    # SHOW FPS ----->
    fps = count / (time.time() - starting_time)
    frame = cv2.putText(frame, 'FPS', (
        center_x + (int(width_f) // 2) - (dr.make_text_size(frame, 'FPS', 0.4, font) + 65),
        center_y - (int(height_f) // 2) + 145), font, 0.4, CYAN, 1, cv2.LINE_AA)
    frame = cv2.putText(frame, (str(int(fps))), (
        center_x + (int(width_f) // 2) - (dr.make_text_size(frame, (str(int(fps))), 0.4, font) + 20),
        center_y - (int(height_f) // 2) + 145), font, 0.4, CYAN, 1, cv2.LINE_AA)
    # <-----

    # SHOW VIDEO SOURCE ----->
    frame = cv2.putText(frame, 'VS', (center_x + (int(width_f) // 2) - (dr.make_text_size(frame, 'VS', 0.4, font) + 65),
                                      center_y - (int(height_f) // 2) + 35), font, 0.4, CYAN, 1, cv2.LINE_AA)
    frame = cv2.putText(frame, (str(VideoSource)), (
        center_x + (int(width_f) // 2) - (dr.make_text_size(frame, (str(VideoSource)), 0.4, font) + 20),
        center_y - (int(height_f) // 2) + 35), font, 0.4, CYAN, 1, cv2.LINE_AA)
    # <-----

    frame = cv2.putText(frame, 'FaustX Technology FX-1ALL', (20, 35), font, 0.4, CYAN, 1, cv2.LINE_AA)
    frame = cv2.putText(frame, ('FX-1 AI v' + str(AI_VAR.ver)) + ' in Test ' + str(AI_VAR.test), (20, 55), font, 0.4,
                        CYAN, 1, cv2.LINE_AA)
    frame = cv2.putText(frame, ("Target(s) in Frame Count: " + str(AI_VAR.tracking_objects)),
                        (20, int(img_h + img_h // 3 + 15)), font, 0.4, CYAN, 1, cv2.LINE_AA)

    frame = dr.make_crosshairs(frame, (top_left_x, top_left_y), (bot_right_x, bot_right_y), CYAN, 1, ctrl_keys[2],
                               center_x, center_y)
    frame = cvzone.overlayPNG(frame, img_logo, [20, int(hb) - hf - 60])

    cv2.imshow("FaustX Tech and Nvidia CUDA - cuDNN Tracking System", frame)

    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    if key == 27:
        print()
        break

cap.release()
cv2.destroyAllWindows()
