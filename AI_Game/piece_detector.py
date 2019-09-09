import cv2
import numpy as np
import circle_detector as cid
import color_detector as cod

def get_piece_num(src_img):
    #Find circles
    ccenters, cradius = cid.find_circles(src_img)
    img_draw = src_img.copy()

    red_num = 0
    green_num = 0
    blue_num = 0
    yellow_num = 0
    #Confirm the color of the piece
    for i in range(len(ccenters)):
        color = cod.color_name(ccenters[i], cradius[i], src_img)
        if color == 'red':
            red_num = red_num + 1
            cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (0, 90, 255), 3)
        if color == 'green':
            green_num = green_num + 1
            cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (90, 255, 0), 3)
        if color == 'blue':
            blue_num = blue_num + 1
            cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (255, 100, 0), 3)
        if color == 'yellow':
            yellow_num = yellow_num + 1
            cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (0, 200, 255), 3)

    return red_num, green_num, blue_num, yellow_num, img_draw


