import cv2
import math
import time
import numpy as np
from drawing_functions import draw as dr

class calc:
    
    def calculate_angle(y, x, fcx, fcy):
        
        x = x - fcx
        y = y - fcy
        
        angle = math.atan2(y, x)
    
        return angle


class telemetry:

    def move_sim_old_version(img, cx, cy, # old version of move_sim circle
                 color, color_l, 
                 img_w, img_h, wh, 
                 fcx, fcy,
                 font):
        
        sim_x = int((cx-fcx))+52
        sim_y = int((cy-fcy))+190
        sim_arrows = list((sim_x, sim_y))
        

        if(sim_x < 24): sim_x = 24
        if(sim_x > 81): sim_x = 81
        
        if(sim_y < 161): sim_y = 161
        if(sim_y > 220): sim_y = 220

        
        if(cx >= fcx-80 and cx <= fcx+80)  and (cy >= fcy-80 and cy <= fcy+80):
            cv2.circle(img, (52, 190), wh, color_l, 1, cv2.LINE_AA)
            cv2.arrowedLine(img, (52, 190), (sim_x, sim_y), color_l, 1, cv2.LINE_AA, 0, 0.1)
        else:
            cv2.arrowedLine(img, (52, 190), (sim_x, sim_y), color, 1, cv2.LINE_AA, 0, 0.1)
            
    def move_sim(img, cx, cy,  #new version of move_sim
                    color, color_l, 
                    img_w, img_h, wh, 
                    fcx, fcy,
                    font):
            
        sim_deg = calc.calculate_angle(cy, cx, fcx, fcy)
        sim_rad = 29
        
        sim_x = int(sim_rad * math.cos(sim_deg))+52
        sim_y = int(sim_rad * math.sin(sim_deg))+190
        

        if(cx >= fcx-80 and cx <= fcx+80)  and (cy >= fcy-80 and cy <= fcy+80):
            cv2.circle(img, (52, 190), wh, color_l, 1, cv2.LINE_AA)
            cv2.arrowedLine(img, (52, 190), (sim_x, sim_y), color_l, 1, cv2.LINE_AA, 0, 0.1)
        else:
            cv2.arrowedLine(img, (52, 190), (sim_x, sim_y), color, 1, cv2.LINE_AA, 0, 0.1)
        
    #TI Protocol
    def identify_target(frame, target_name, cls_id, font, 
                        color, color_1, x, y,
                        cx, cy):
        
        if cls_id == 4:
            dr.draw_text_w_r(frame, "TIP ORDER: "+target_name+": Allied", x, y-15, color, color_1, -1, font)
        if cls_id == 0:
            dr.draw_text_w_r(frame, "TIP ORDER: "+target_name+": TRACK HIM", x, y-15, color, color_1, -1, font)
        if cls_id == 2:
            dr.draw_text_w_r(frame, "TIP ORDER: "+target_name+" "+str(cls_id), x, y-15, color, color_1, -1, font)
            
    def calc_yaw(raw_yaw, heading):
        
        if(heading):
            yaw = str(heading)
            
        else: 
            if (raw_yaw < 0):
                yaw = 360+((raw_yaw*180)//math.pi)
            else:
                yaw = (raw_yaw*180)//math.pi
                
        if(yaw == float(0.0)):
            yaw = "0"
        return yaw
    
    def calc_pitch(raw_pitch):
        
        pitch = (raw_pitch*180)//math.pi
        
        return pitch
    
    def calc_roll(raw_roll):
        
        roll = (raw_roll*180)//math.pi
         
        return roll
            
    def ekf_status(vehicle):
        if(vehicle):
            EKF = 'OK'
        else:
            EKF = 'ERR'
            
        return EKF
    
    def armed_status(vehicle):
        if(vehicle):
            ARM = 'ARMED'
        else:
            ARM = 'DISARMED'
            
        return ARM
    
    def TIME_MODULE(img, color, time_data, isonline, fcx, fcy, font):
        
        if(isonline):
            time_zone = "("+str(time_data[-1][0])+")"
            time_s = str(time_data[-1][1])
            
            img = cv2.putText(img, ('CLK '+time_zone), (fcx+190, fcy+230), font, 0.4, color,1 ,cv2.LINE_AA)
            img = cv2.putText(img, (time_s), (fcx+190, fcy+250), font, 0.4, color,1 ,cv2.LINE_AA)
        else:
            img = cv2.putText(img, (time_data), (fcx+190, fcy+230), font, 0.4, color,1 ,cv2.LINE_AA)
        
        return img


    def return_autopilot_msg(img, msg, font, center_x, center_y, color):

        img = cv2.putText(img, str(msg), (dr.make_text_center(img, str(msg), 0.5,1, font), center_y+80), font, 0.5, color,1 ,cv2.LINE_AA)

    

    
            



