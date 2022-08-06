import cv2
import numpy as np
import math
from math import sin, cos


class draw:

    @staticmethod
    def make_logo():

        img_logo = cv2.imread("parts/images/fx-logo-c.png", cv2.IMREAD_UNCHANGED)
        img_logo = cv2.resize(img_logo, (0, 0), None, 0.5, 0.5)

        return img_logo

    @staticmethod
    def make_logo_w():

        img_logo = cv2.imread("parts/images/fx-logo-w.png", cv2.IMREAD_UNCHANGED)
        img_logo = cv2.resize(img_logo, (0, 0), None, 0.5, 0.5)

        return img_logo

    def make_crosshairs(img, track_x, track_y, ch_color, captured, mode, fcx, fcy):

        if (mode == 1):
            img = cv2.line(img, (fcx - 10, fcy), (fcx - 30, fcy), ch_color, 1, cv2.LINE_AA)

            img = cv2.line(img, (fcx, fcy - 10), (fcx, fcy - 30), ch_color, 1, cv2.LINE_AA)
            img = cv2.line(img, (fcx + 30, fcy), (fcx + 10, fcy), ch_color, 1, cv2.LINE_AA)

            img = cv2.line(img, (fcx, fcy + 30), (fcx, fcy + 10), ch_color, 1, cv2.LINE_AA)

        return img

    def make_target_track(img, color, x, y, w, h, cx, cy):

        cv2.line(img, (x, y), (x, y + h // 4), color, 1)  # -- top-left
        cv2.line(img, (x, y), (x + h // 4, y), color, 1)

        cv2.line(img, (x + w, y + h), (x + w, y + h - h // 4), color, 1)  # -- bottom-right
        cv2.line(img, (x + w, y + h), (x + w - h // 4, y + h), color, 1)

        cv2.line(img, (x, y + h), (x, y + h - h // 4), color, 1)  # -- bottom-left
        cv2.line(img, (x, y + h), (x + h // 4, y + h), color, 1)

        cv2.line(img, (x + w, y), (x + w - h // 4, y), color, 1)  # -- top-right
        cv2.line(img, (x + w, y), (x + w, y + h // 4), color, 1)

        return img

    def shoot_cross(img, cx, cy, color):
        # Center Cross
        cv2.line(img, (cx - 5, cy), (cx - 10, cy), color, 1)

        cv2.line(img, (cx, cy - 5), (cx, cy - 10), color, 1)
        cv2.line(img, (cx + 5, cy), (cx + 10, cy), color, 1)

        cv2.line(img, (cx, cy + 10), (cx, cy + 5), color, 1)

        return img

    def draw_text_w_r(img, text, posx, posy, text_color, text_color_bg, rec, font, font_scale=0.4, font_thickness=1):

        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        if (rec == 2):
            ss = 1
        else:
            cv2.rectangle(img, (posx - 6, posy - 6), (posx + text_w, posy + text_h), text_color_bg, rec, cv2.LINE_AA)

        cv2.putText(img, str(text), (posx - 3, posy + text_h - 3), font, font_scale, text_color, font_thickness,
                    cv2.LINE_AA)

        return text_size

    def make_text_center(frame, text, fsize, param, font):

        text_f = text;
        # get boundary of this text
        textsize = cv2.getTextSize(text_f, font, fsize, 1)[0]

        # get coords based on boundary
        textX = round((frame.shape[1] - textsize[0]) / 2)
        textY = round((frame.shape[0] + textsize[1]) / 2)

        if (param == 1):
            result = textX
        else:
            result = textX, textY

        return result

    def make_text_size(frame, text, fsize, font):
        text_f = text;
        # get boundary of this text
        textsize = cv2.getTextSize(text_f, font, fsize, 1)[0]

        # get coords based on boundary
        textX = textsize[0]

        result = textX
        return result

    def make_move_sim_circle(img, color, font):

        img = cv2.circle(img, (52, 190), 30, color, 1, cv2.LINE_AA)
        img = cv2.circle(img, (52, 190), 1, color, -1, cv2.LINE_AA)
        img = cv2.line(img, (52, 165), (52, 157), color, 1, cv2.LINE_AA)
        img = cv2.line(img, (52, 215), (52, 223), color, 1, cv2.LINE_AA)

        img = cv2.line(img, (77, 190), (85, 190), color, 1, cv2.LINE_AA)
        img = cv2.line(img, (27, 190), (19, 190), color, 1, cv2.LINE_AA)

        return img

    def lock_anim(img, color, wh, fcx, fcy):

        img = cv2.line(img, (fcx - 110 - wh, fcy + 50), (fcx - 110 - wh, fcy - 50), color, 1)
        img = cv2.line(img, (fcx + 110 + wh, fcy + 50), (fcx + 110 + wh, fcy - 50), color, 1)

        img = cv2.line(img, (fcx - 110 - wh, fcy + 30), (fcx - 110 - wh, fcy - 30), color, 1)
        img = cv2.line(img, (fcx + 110 + wh, fcy + 30), (fcx + 110 + wh, fcy - 30), color, 1)

        return img

    def textBlurBackground(img, text, font, fontScale, textPos, textColor, textThickness=1, kneral=(63, 63), pad_x=3,
                           pad_y=3):

        (t_w, t_h), _ = cv2.getTextSize(text, font, fontScale, textThickness)  # getting the text size

        x, y = textPos
        blur_roi = img[y - pad_y - t_h: y + pad_y, x - pad_x:x + t_w + pad_x]  # croping Text Background
        img[y - pad_y - t_h: y + pad_y, x - pad_x:x + t_w + pad_x] = cv2.blur(blur_roi,
                                                                              kneral)  # merging the blured background to img
        cv2.putText(img, text, textPos, font, fontScale, textColor, textThickness)

        return img

    def ktas_alt_frame(img, color, fcx, fcy, font, for_ktas):

        img = cv2.line(img, (fcx - 190, fcy + 160), (fcx - 190, fcy - 160), color, 1, cv2.LINE_AA)  # Left
        img = cv2.line(img, (fcx + 190, fcy + 160), (fcx + 190, fcy - 160), color, 1, cv2.LINE_AA)  # Right

        img = cv2.line(img, (fcx - 190, fcy - 160), (fcx - 240, fcy - 160), color, 1, cv2.LINE_AA)  # Left Top
        img = cv2.line(img, (fcx + 190, fcy - 160), (fcx + 240, fcy - 160), color, 1, cv2.LINE_AA)  # Right Top

        img = cv2.line(img, (fcx - 190, fcy + 160), (fcx - 240, fcy + 160), color, 1, cv2.LINE_AA)  # Left Bottom
        img = cv2.line(img, (fcx + 190, fcy + 160), (fcx + 240, fcy + 160), color, 1, cv2.LINE_AA)  # Right Bottom

        # ALT Text
        img = cv2.putText(img, ('ALT HM'), (fcx + 190, fcy - 175), font, 0.4, color, 1, cv2.LINE_AA)
        img = cv2.putText(img, ('TAS/M'), (fcx - 190 - for_ktas, fcy - 175), font, 0.4, color, 1, cv2.LINE_AA)

        img = cv2.arrowedLine(img, (fcx - 240, fcy + 2), (fcx - 239, fcy + 2), color, 1, cv2.LINE_AA, 0, 8)
        img = cv2.arrowedLine(img, (fcx + 240, fcy + 2), (fcx + 239, fcy + 2), color, 1, cv2.LINE_AA, 0, 8)

        return img

    def clamp(n, minn, maxn):  # Limit a number
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        else:
            return n

    def GPI_VZ_ALT(img, color, fcx, fcy, vz):

        vz = int(vz) // 3
        vz = draw.clamp(vz, -150, 150)

        img = cv2.arrowedLine(img, (fcx + 240, (fcy + 2) + vz), (fcx + 239, (fcy + 2) + vz), color, 1, cv2.LINE_AA, 0,
                              8)

        return img

    def drawline_d(img, pt1, pt2, color, gap=5, thickness=1, style='line'):

        dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** .5
        pts = []
        for i in np.arange(0, dist, gap):
            r = i / dist
            x = int((pt1[0] * (1 - r) + pt2[0] * r) + .5)
            y = int((pt1[1] * (1 - r) + pt2[1] * r) + .5)
            p = (x, y)
            pts.append(p)

        if style == 'dotted':
            for p in pts:
                img = cv2.circle(img, p, thickness, color, -1)
        else:
            s = pts[0]
            e = pts[0]
            i = 0
            for p in pts:
                s = e
                e = p
                if i % 2 == 1:
                    img = cv2.line(img, s, e, color, thickness, cv2.LINE_AA)
                i += 1
        return img

    def drawline_d_for_red_roll(img, pt1, pt2, color, color_2, color_3, gap=5, thickness=1, style='line'):

        dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** .5
        pts = []
        for i in np.arange(0, dist, gap):
            r = i / dist
            x = int((pt1[0] * (1 - r) + pt2[0] * r) + .5) + 10
            y = int((pt1[1] * (1 - r) + pt2[1] * r) + .5)
            p = (x, y)
            pts.append(p)

        if style == 'dotted':
            for p in pts:
                img = cv2.circle(img, p, thickness, color, -1)
        else:
            s = pts[0]
            e = pts[0]
            i = 0
            for p in pts:
                s = e
                e = p
                if i % 2 == 1:

                    if (i == 1):
                        img = cv2.line(img, s, e, color_3, thickness, cv2.LINE_AA)
                    if (i == 11):
                        img = cv2.line(img, s, e, color_3, thickness, cv2.LINE_AA)
                i += 1
        return img


class text_details():

    def right_allign_text(self, img, text, color, center_x, center_y,
                          wf, hf, font, xpos, ypos):
        text = str(text)
        img = cv2.putText(img, (text), (
        center_x + (int(wf) // 2) - (draw.make_text_size(img, (text), 0.4, font) + xpos),
        center_y - (int(hf) // 2) + ypos), font, 0.4, color, 1, cv2.LINE_AA)

        return img


class round_inducators:

    def inducator_color(self, data):

        if (data == "NORM"):
            color = (240, 240, 0)
        elif (data == "WARN"):
            color = (0, 240, 240)
        elif (data == "CRIT"):
            color = (0, 0, 240)
        else:
            color = (240, 240, 0)
        return color

    def check_called_data(self, bunelen, Angle1, Angle2, sys_time):

        if (bunelen == "throttle_data"):

            Angle1 = int(Angle1 / 2.7)
            style_text = "THRTL"
            text = " " + str(Angle1) + "% "
            reverse = 0
            if (Angle1 >= 100):
                info_text = "FULL"
                incolor = self.inducator_color("CRIT")
            else:
                info_text = None
                incolor = self.inducator_color("NORM")

        if (bunelen == "rpm_data"):

            Angle1 = Angle2
            style_text = "RPM"
            text = " " + str(Angle1) + " "
            reverse = 0
            if (Angle1 >= 5200):
                info_text = "HIGH"
                incolor = self.inducator_color("WARN")
            else:
                info_text = None
                incolor = self.inducator_color("NORM")

        if (bunelen == "fuel_data"):

            Angle1 = Angle2
            style_text = "FUEL"
            text = " " + str(Angle1) + "% "
            reverse = 1
            if (Angle1 <= 50):
                if (Angle1 <= 20):
                    info_text = "CRIT"
                    if ((sys_time % 2) == 0):

                        incolor = self.inducator_color("CRIT")
                    else:

                        incolor = self.inducator_color("WARN")
                else:
                    info_text = "WARN"
                    incolor = self.inducator_color("WARN")
            else:
                info_text = None
                incolor = self.inducator_color("NORM")

        if (bunelen == "absp_data"):

            Angle1 = Angle2
            style_text = "ABS P"
            text = " " + str(Angle1) + " "
            reverse = 0
            if (Angle1 >= 5200):
                info_text = "HIGH"
                incolor = self.inducator_color("WARN")
            else:
                info_text = None
                incolor = self.inducator_color("NORM")

        return (text, style_text, info_text, reverse, incolor)

    def draw_round_inducator_dynamic(self, img, xpos, ypos,
                                     color, color_2, color_3, radius, startAngle, thickness, endAngle=270):

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2

        # Ellipse parameters
        axes = (radius, radius)
        angle = 270
        img = cv2.ellipse(img, (cf_cx + xpos, cf_cy + ypos), axes, angle, startAngle, endAngle, color, thickness,
                          cv2.LINE_AA)

        return img

    def draw_round_inducator_main_static(self, img, xpos, ypos,
                                         color, color_2, color_3, font,
                                         Angle1, Angle2, bunelen, endAngle_R, endAngle_O, endAngle_C,
                                         R_eA_R=0, R_eA_O=0, R_eA_C=0, sys_time=0,
                                         startAngle=0, thickness=1,
                                         radius=40):

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2
        DarkedColor_CYAN = (130, 130, 0)
        DarkedColor_RED = (0, 0, 150)
        DarkedColor_ORANGE = (0, 150, 150)
        angle = 270

        # check called data

        data_text, style_text, info_text, reverse, incolor = self.check_called_data(bunelen, Angle1, Angle2, sys_time)

        # do reverse when required

        if (reverse == 1):
            endAngle_R, endAngle_O, endAngle_C = (angle, angle, angle)
            startAngle_R, startAngle_O, startAngle_C = (R_eA_R, R_eA_O, R_eA_C)
        else:
            startAngle_R, startAngle_O, startAngle_C = (startAngle, startAngle, startAngle)

        # ellipse parameters
        axes = (radius, radius)

        # make data text(s) - text datası 5 basamaktan fazla olmamalı
        calc_text_pos_data = int(draw.make_text_size(img, str(data_text), 0.4, font) // 2) - 3
        calc_text_pos_style = int(draw.make_text_size(img, str(style_text), 0.3, font) // 2) - 1

        draw.draw_text_w_r(img, str(data_text), (cf_cx + xpos) - calc_text_pos_data, (cf_cy + ypos - 8), color, incolor,
                           1, font)
        # img = cv2.circle(img, (cf_cx+xpos, cf_cy+ypos), 2, (0, 0, 255), -1)
        # make style text(s) - text style'ı 5 basamaktan fazla olmamalı, uzunsa baş harflerini kullan
        img = cv2.putText(img, str(style_text), ((cf_cx + xpos) - calc_text_pos_style, (cf_cy + ypos + 20)), font, 0.3,
                          color, 1, cv2.LINE_AA)
        if (info_text):
            img = cv2.putText(img, str(info_text), ((cf_cx + xpos - 37), (cf_cy + ypos) - 35), font, 0.3, incolor, 1,
                              cv2.LINE_AA)

        # make rounds
        img = cv2.ellipse(img, (cf_cx + xpos, cf_cy + ypos), axes, angle, startAngle_R, endAngle_R, DarkedColor_RED,
                          thickness, cv2.LINE_AA)
        img = cv2.ellipse(img, (cf_cx + xpos, cf_cy + ypos), axes, angle, startAngle_O, endAngle_O, DarkedColor_ORANGE,
                          thickness, cv2.LINE_AA)
        img = cv2.ellipse(img, (cf_cx + xpos, cf_cy + ypos), axes, angle, startAngle_C, endAngle_C, DarkedColor_CYAN,
                          thickness, cv2.LINE_AA)
        img = self.draw_round_inducator_dynamic(img, xpos, ypos, color, color_2, color_3, radius, startAngle, thickness,
                                                endAngle=Angle1)

        return img


class ahrs:

    def to_yaw_string(self, fb_count):
        if fb_count % 4 == 1:
            return "W"
        elif fb_count % 4 == 2:
            return "S"
        elif fb_count % 4 == 3:
            return "E"
        elif fb_count % 4 == 0:
            return "N"
        else:
            return "ERR"

    def make_ahrs_compass(self, img, color, color_2, fcx, fcy, yaw, font):
        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2

        if (str(yaw)):  # Ortadaki yaw datası
            img = cv2.line(img, (cf_cx, 55), (cf_cx, 70), color_2, 1, cv2.LINE_AA)
            img = cv2.arrowedLine(img, (cf_cx, 47), (cf_cx, 48), color, 1, cv2.LINE_AA, 0, 7)
            img = cv2.putText(img, str(int(yaw)), (draw.make_text_center(img, str(int(yaw)), 0.5, 1, font) + 1, 35),
                              font, 0.5, color, 1, cv2.LINE_AA)

        # -->
        # Kalibrasyon için deger parametresine - veya + değer verilerek headling ayarlanabilir.
        deger = 0
        fb_count = 0

        yaw = int(yaw)
        calculated_yaw = int((yaw % 180))

        if yaw == 360:
            calculated_yaw = 0
        elif yaw == 180:
            calculated_yaw = 180
        elif yaw > 180:
            calculated_yaw = -(180 - calculated_yaw)

        for a in range(calculated_yaw - 990, calculated_yaw + 990, 15):
            img = cv2.line(img, (cf_cx - a - deger, 55), (cf_cx - a - deger, 61), color, 1)  # mid line

        for b in range(calculated_yaw - 990, calculated_yaw + 990, 90):
            fb_count += 1

            img = cv2.line(img, (cf_cx - b - deger, 55), (cf_cx - b - deger, 70), color, 1, cv2.LINE_AA)  # long line
            img = cv2.putText(img, (self.to_yaw_string(fb_count)), (cf_cx - b - 5 - deger, 88), font, 0.5, color, 1,
                              cv2.LINE_AA)

        return img

    def make_ahrs_alt(self, img, color, color_2, color_3, fcx, fcy, alt, font):

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2
        value = int(-16000)
        x_sabiti_start = 1
        x_sabiti_end = 10

        alt = int(alt)
        calc_alt = alt * 5

        if (str(alt)):
            # print(cf_cx)
            img = cv2.line(img, (x_sabiti_start, cf_cy), (x_sabiti_end, cf_cy), color_2, 1, cv2.LINE_AA)

        for a in range(calc_alt + 80000, calc_alt - 80000, -25):

            if (cf_cy + a < cf_cy - 170 or cf_cy + a < cf_cy + 170):

                if (int(value) % 10 == 0):

                    if (value == alt):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color_2, 1,
                                       cv2.LINE_AA)
                        img = cv2.putText(img, str(int(value)), (x_sabiti_end + 3, cf_cy + a + 3), font, 0.3, color_2,
                                          1, cv2.LINE_AA)
                    elif (value >= 0):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color, 1,
                                       cv2.LINE_AA)
                        img = cv2.putText(img, str(int(value)), (x_sabiti_end + 3, cf_cy + a + 3), font, 0.3, color, 1,
                                          cv2.LINE_AA)
                    else:
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color, 1,
                                       cv2.LINE_AA)
                        img = cv2.putText(img, str(int(value)), (x_sabiti_end + 3, cf_cy + a + 3), font, 0.3, color, 1,
                                          cv2.LINE_AA)

                elif (int(value) % 5 == 0):

                    if (value == alt):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color_2, 1,
                                       cv2.LINE_AA)
                    elif (value >= 0):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color, 1,
                                       cv2.LINE_AA)
                    else:
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color, 1,
                                       cv2.LINE_AA)

            value += 5
        return img

    def make_ahrs_tas(self, img, color, color_2, color_3, fcx, fcy, speed, font):

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2
        value = int(-180)
        x_sabiti_start = 37
        x_sabiti_end = 46

        speed = int(speed)
        calc_speed = speed * 5

        if (str(speed)):
            # print(cf_cx)
            img = cv2.line(img, (x_sabiti_start, cf_cy), (x_sabiti_end, cf_cy), color_2, 1, cv2.LINE_AA)

        for a in range(calc_speed + 900, calc_speed - 900, -25):

            if (cf_cy + a < cf_cy - 170 or cf_cy + a < cf_cy + 170):

                if (int(value) % 10 == 0):

                    if (value == speed):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color_2, 1,
                                       cv2.LINE_AA)
                        img = cv2.putText(img, str(int(value)), (
                        x_sabiti_end - draw.make_text_size(img, str(int(value)), 0.3, font) - 11, cf_cy + a + 3), font,
                                          0.3, color_2, 1, cv2.LINE_AA)
                    elif (True):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color, 1,
                                       cv2.LINE_AA)
                        img = cv2.putText(img, str(int(value)), (
                        x_sabiti_end - draw.make_text_size(img, str(int(value)), 0.3, font) - 11, cf_cy + a + 3), font,
                                          0.3, color, 1, cv2.LINE_AA)

                elif (int(value) % 5 == 0):

                    if (value == speed):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color_2, 1,
                                       cv2.LINE_AA)
                    elif (True):
                        img = cv2.line(img, (x_sabiti_start, cf_cy + a), (x_sabiti_end, cf_cy + a), color, 1,
                                       cv2.LINE_AA)

            value += 5
        return img

    def rotateAndScale(self, img, scaleFactor=0.5, degreesCCW=30):

        oldY, oldX = img.shape[0], img.shape[1]  # note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
        M = cv2.getRotationMatrix2D(center=(oldX / 2, oldY / 2), angle=degreesCCW,
                                    scale=scaleFactor)  # rotate about center of image.

        # choose a new image size.
        newX, newY = oldX * scaleFactor, oldY * scaleFactor
        # include this if you want to prevent corners being cut off
        r = np.deg2rad(degreesCCW)
        newX, newY = (abs(np.sin(r) * newY) + abs(np.cos(r) * newX), abs(np.sin(r) * newX) + abs(np.cos(r) * newY))

        # the warpAffine function call, below, basically works like this:
        # 1. apply the M transformation on each pixel of the original image
        # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

        # So I will find the translation that moves the result to the center of that region.
        (tx, ty) = ((newX - oldX) / 2, (newY - oldY) / 2)
        M[0, 2] += tx  # third column of matrix holds translation, which takes effect after rotation.
        M[1, 2] += ty

        rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX), int(newY)))
        return rotatedImg

    def make_ahrs_roll_and_pitch_bars(self, img, color,
                                      color_2, color_3,
                                      fcx, fcy, roll,
                                      pitch, font):

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2
        value = int(-120)

        theta = np.deg2rad(roll)
        rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

        pitch = int(pitch) * 6
        c = np.array([cf_cx, cf_cy])

        for a in range(720, -720, -30):

            vsl_1_L_S = np.dot(rot, np.array([-40, a + pitch - 6])).astype(int)
            vsl_1_L_E = np.dot(rot, np.array([-40, a + pitch + 6])).astype(int)

            vsl_1_R_S = np.dot(rot, np.array([+40, a + pitch - 6])).astype(int)
            vsl_1_R_E = np.dot(rot, np.array([+40, a + pitch + 6])).astype(int)

            hll_1_L_E = np.dot(rot, np.array([-100, a + pitch - 6])).astype(int)
            hll_1_R_E = np.dot(rot, np.array([+100, a + pitch - 6])).astype(int)

            hll_D_1_L_E = np.dot(rot, np.array([-100, a + pitch + 12])).astype(int)
            hll_D_1_R_E = np.dot(rot, np.array([+100, a + pitch + 12])).astype(int)

            txt_1_R_P = np.dot(rot, np.array([+47, a + pitch + 12])).astype(int)
            txt_1_R_M = np.dot(rot, np.array([+47, a + pitch - 5])).astype(int)

            if (int(value) % 10 == 5):

                Dont_Draw_This_Lines = 1

            elif (int(value) == 0):
                point_0_S = np.dot(rot, np.array([-360, a + pitch])).astype(int)
                point_0_E = np.dot(rot, np.array([+360, a + pitch])).astype(int)

                point_0_R_S = np.dot(rot, np.array([-360, 0])).astype(int)
                point_0_R_E = np.dot(rot, np.array([+360, 0])).astype(int)

                img = cv2.line(img, (c + point_0_S), (c + point_0_E), color, 1, cv2.LINE_AA)
                img = cv2.line(img, (c + point_0_R_S), (c + point_0_R_E), color_3, 1, cv2.LINE_AA)

            elif (int(value) < 0):

                img = cv2.line(img, (c + vsl_1_L_S), (c + vsl_1_L_E), color, 1, cv2.LINE_AA)
                img = draw.drawline_d(img, (c + vsl_1_L_E), (c + hll_D_1_L_E), color, 5)

                img = cv2.line(img, (c + vsl_1_R_S), (c + vsl_1_R_E), color, 1, cv2.LINE_AA)
                img = draw.drawline_d(img, (c + vsl_1_R_E), (c + hll_D_1_R_E), color, 5)

                txt_1_L_M = np.dot(rot, np.array(
                    [-47 - draw.make_text_size(img, str(int(value)), 0.3, font), a + pitch - 5])).astype(int)
                img = cv2.putText(img, str(int(value)), (c + txt_1_L_M), font, 0.3, color, 1, cv2.LINE_AA)
                img = cv2.putText(img, str(int(value)), (c + txt_1_R_M), font, 0.3, color, 1, cv2.LINE_AA)

            else:

                img = cv2.line(img, (c + vsl_1_L_S), (c + vsl_1_L_E), color, 1, cv2.LINE_AA)
                img = cv2.line(img, (c + vsl_1_L_S), (c + hll_1_L_E), color, 1, cv2.LINE_AA)

                img = cv2.line(img, (c + vsl_1_R_S), (c + vsl_1_R_E), color, 1, cv2.LINE_AA)
                img = cv2.line(img, (c + vsl_1_R_S), (c + hll_1_R_E), color, 1, cv2.LINE_AA)

                txt_1_L_P = np.dot(rot, np.array(
                    [-47 - draw.make_text_size(img, str(int(value)), 0.3, font), a + pitch + 12])).astype(int)
                img = cv2.putText(img, str(int(value)), (c + txt_1_L_P), font, 0.3, color, 1, cv2.LINE_AA)
                img = cv2.putText(img, str(int(value)), (c + txt_1_R_P), font, 0.3, color, 1, cv2.LINE_AA)
            value += 5

        return img

    def red_roll_line(self, img, color, color_2, color_3, roll):

        theta = np.deg2rad(roll)
        rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2
        c = np.array([cf_cx, cf_cy])

        RRL_S = np.dot(rot, np.array([-418, 0])).astype(int)
        RRL_E = np.dot(rot, np.array([+418, 0])).astype(int)

        img = draw.drawline_d_for_red_roll(img, (c + RRL_S), (c + RRL_E), color, color_2, color_3, 75)

        return img

    def make_aoa_ssa_vector(self, img, color, color_2, color_3, aoa, ssa, climb, font):

        # AOA SSA VECTOR POINT AREA ----->
        climb = int(climb)
        raw_aoa = abs(int(aoa))
        aoa = int(aoa) * int(math.pi * 2.5)
        ssa = int(ssa) * int(math.pi * 2)

        cf_cy, cf_cx = img.shape[0] // 2, img.shape[1] // 2

        img = cv2.circle(img, (cf_cx + ssa, cf_cy + aoa), 8, color_3, 1, cv2.LINE_AA)

        img = cv2.line(img, ((cf_cx + 8) + ssa, (cf_cy) + aoa), ((cf_cx + 20) + ssa, (cf_cy) + aoa), color_3, 1,
                       cv2.LINE_AA)
        img = cv2.line(img, ((cf_cx - 8) + ssa, (cf_cy) + aoa), ((cf_cx - 20) + ssa, (cf_cy) + aoa), color_3, 1,
                       cv2.LINE_AA)

        img = cv2.line(img, ((cf_cx) + ssa, (cf_cy) + aoa - 8), ((cf_cx) + ssa, (cf_cy) + aoa - 20), color_3, 1,
                       cv2.LINE_AA)
        # <-----
        # SHOW AOA DEG DATA AREA ----->
        draw.draw_text_w_r(img, ("AOA " + str(raw_aoa)),
                           cf_cx - 190 - draw.make_text_size(img, "AOA " + str(raw_aoa), 0.4, font), cf_cy + 205, color,
                           color, 2, font)
        # <-----

        return img
