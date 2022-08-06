from detection_systems.object_detection import ObjectDetection, KalmanFilter, BgDetector
from functions.telemetry_functions import telemetry as tl
from functions.drawing_functions import text_details ,draw as dr
import cv2
import winsound

od = ObjectDetection()
kf = KalmanFilter()
bg = BgDetector()
dr_td = text_details()

class lcl_var:
    
    lock_range = 70
    lock_range_circle = 23
    tracking_objects = 0
    ver = "OpenFX 1.6.5"
    test = "NO_TEST_NUMBER_GIVEN"

class FX1AI_MAIN():
    
    def __init__(self, frame, width_f, height_f, proximity, ctrl_keys, 
                 CYAN, BLACK, ORANGE, WHITE, GREEN, RED,
                 font, center_points_cur_frame, 
                 center_x, center_y, in_range, in_lock,
                 track_id, count):
        
        self.frame = frame
        self.width_f = width_f
        self.height_f = height_f
        self.proximity = proximity
        self.ctrl_keys = ctrl_keys
        self.CYAN = CYAN
        self.BLACK = BLACK
        self.ORANGE = ORANGE
        self.WHITE = WHITE
        self.GREEN = GREEN
        self.RED = RED
        self.font = font
        self.center_points_cur_frame = center_points_cur_frame
        self.center_x = center_x
        self.center_y = center_y
        self.track_id = track_id
        self.count = count
        self.in_range = in_range
        self.in_lock = in_lock
        (self.class_ids, self.scores, self.boxes) = od.detect(self.frame)
        
    def __call__(self):
        for (class_id, score, box) in zip(self.class_ids, self.scores, self.boxes):
            (x, y, w, h) = box
            if((w < self.width_f//2 and h < self.height_f//2) or self.proximity == 0):
                    cx = int((x + x + w) / 2)
                    cy = int((y + y + h) / 2)
                    
                    target_name = od.classes[int(class_id)]
                    lcl_var.tracking_objects = len(self.class_ids)

                    if(self.ctrl_keys[4] == 1):
                        tl.identify_target(self.frame, target_name, int(class_id), self.font, self.BLACK, self.ORANGE, x, y, cx, cy)
                    
                    self.center_points_cur_frame.append((cx, cy))
                    detected_ids = [s for s in str(self.class_ids) if s.isdigit()]
                    label = list(map(int, detected_ids))
                    
                    tl.move_sim(self.frame, cx, cy, self.CYAN, self.ORANGE, self.width_f, self.height_f, lcl_var.lock_range_circle, self.center_x, self.center_y, self.font)
                    if(self.ctrl_keys[1] == True):
                        dr.make_target_track(self.frame, self.RED, x, y, w, h, cx, cy)
                    if(self.ctrl_keys[0] == True):
                        cv2.line(self.frame, (cx, cy), (self.center_x, self.center_y), (0, 255, 0), 1, cv2.LINE_AA)
                        cv2.circle(self.frame, (cx,cy), 2, (0, 0, 255), -1, cv2.LINE_AA)
                    if(self.ctrl_keys[0] == False and self.ctrl_keys[1] == False):
                        self.in_range = True
                    if((self.ctrl_keys[0] == True or self.ctrl_keys[1] == True) and self.ctrl_keys[3] == 1):
                        
                         if(cx >= self.center_x-80 and cx <= self.center_x+80)  and (cy >= self.center_y-80 and cy <= self.center_y+80):
                             cv2.rectangle(self.frame, (x, y), (x + w, y + h), self.ORANGE, 1)
                             cv2.line(self.frame, (cx, cy), (self.center_x, self.center_y), self.ORANGE, 1)
                             cv2.circle(self.frame, (cx,cy), 2, (0, 0, 255), -1)
                             self.in_lock = True
            else: 
                self.frame = cv2.putText(self.frame, ('PROXIMITY ERROR'), (self.center_x+(int(self.width_f)//2)-(dr.make_text_size(self.frame, ('PROXIMITY ERROR'), 0.4, self.font)+20), self.center_y-(int(self.height_f)//2)+185), self.font, 0.4, self.ORANGE,1 ,cv2.LINE_AA)
            
        if(lcl_var.lock_range == 20): lcl_var.lock_range = 70
        if(lcl_var.lock_range_circle == 5): lcl_var.lock_range_circle = 23
                
        if(self.in_range == True):
                
            dr.draw_text_w_r(self.frame, 'TARGET(S) IN RANGE', int((self.center_x+(int(self.width_f)//2)-(dr.make_text_size(self.frame, ('TARGET(S) IN RANGE'), 0.4, self.font)+20))),int(( self.center_y-(int(self.height_f)//2)+220)), self.BLACK, self.ORANGE, -1, self.font)
        if(self.in_lock == True):
                
            lcl_var.lock_range -= 1
            lcl_var.lock_range_circle -= 1
            dr.draw_text_w_r(self.frame, 'FALS INIT', 97,164, self.BLACK, self.ORANGE, -1, self.font)
            self.frame = cv2.putText(self.frame, 'KEEP CENTER', (dr.make_text_center(self.frame, 'KEEP CENTER', 0.4,1, self.font), self.center_y+110), self.font, 0.4, self.ORANGE,1 ,cv2.LINE_AA)

            #koy
            dr.lock_anim(self.frame, self.ORANGE, lcl_var.lock_range, self.center_x, self.center_y)
            if(self.count % 15) == 5:
                        
                winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
                            
        # FALS ON OFF ---->
        dr_td.right_allign_text(self.frame, 'FALS', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 65, 105)

        if(self.ctrl_keys[3] == 1):
            dr_td.right_allign_text(self.frame, 'ON', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 20, 105)
        else:
            dr_td.right_allign_text(self.frame, 'OFF', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 20, 105)
            lcl_var.lock_range = 70
            lcl_var.lock_range_circle = 23
        # <-----
        #TIP ON OFF ----->
        dr_td.right_allign_text(self.frame, 'TIP', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 65, 125)

        if(self.ctrl_keys[4] == 1):
            dr_td.right_allign_text(self.frame, 'ON', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 20, 125)
        else:
            dr_td.right_allign_text(self.frame, 'OFF', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 20, 125)
        #<-----
        #SHOW CTH ----->
        dr_td.right_allign_text(self.frame, 'CTH', self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 65, 165)
        dr_td.right_allign_text(self.frame, (str(od.confThreshold)), self.CYAN, self.center_x, self.center_y, self.width_f,self.height_f, self.font, 20, 165)
        #<-----

        # SHOW CUDNN ----->
        self.frame = cv2.putText(self.frame, ('CDN'), (self.center_x + (int(self.width_f) // 2) - (dr.make_text_size(self.frame, ('CDN'), 0.4, self.font) + 65), self.center_y - (int(self.height_f) // 2) + 55), self.font, 0.4, self.CYAN, 1, cv2.LINE_AA)
        self.frame = cv2.putText(self.frame, ('AUTO'), (self.center_x + (int(self.width_f) // 2) - (dr.make_text_size(self.frame, ('AUTO'), 0.4, self.font) + 20), self.center_y - (int(self.height_f) // 2) + 55), self.font, 0.4, self.CYAN, 1, cv2.LINE_AA)
        # <-----

        # SHOW DEPTH ----->
        self.frame = cv2.putText(self.frame, ('DEP'), (self.center_x + (int(self.width_f) // 2) - (dr.make_text_size(self.frame, ('DEP'), 0.4, self.font) + 65), self.center_y - (int(self.height_f) // 2) + 75), self.font, 0.4, self.CYAN, 1, cv2.LINE_AA)
        self.frame = cv2.putText(self.frame, ('AUTO'), (self.center_x + (int(self.width_f) // 2) - (dr.make_text_size(self.frame, ('AUTO'), 0.4, self.font) + 20), self.center_y - (int(self.height_f) // 2) + 75), self.font, 0.4, self.CYAN, 1, cv2.LINE_AA)
        # <-----


