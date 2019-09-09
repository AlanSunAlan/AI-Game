#! /usr/bin/env python3

from selenium import webdriver
import _thread
import time
import piece_detector as pd
import cv2
import pyrealsense2 as rs
import numpy as np

red = green = blue = yellow = 0
start = False

def click(browser, times, xpath):
    if times > 0:
        for i in range(1, times):
            button = browser.find_element_by_xpath(xpath)
            button.click()

##############################################
###To determine if there is object in place###
def objectFound(pipeline):
    global red, green, blue, yellow
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            # Convert realsense images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())

            red, green, blue, yellow, img_draw = pd.get_piece_num(color_image)
            cv2.imshow('Detection Result', img_draw)
            cv2.waitKey(1)


    finally:
        pipeline.stop()




##############################################
#Thread being triggered when object is found##
def triggerFunc():
    global red, green, blue, yellow, start
    #Open playground
    browser = webdriver.Firefox() # Get local session of firefox
    browser.get("file:///home/alan/developing/AI_Game/dist/index.html") # Load page

    browser.maximize_window()

    #Time interval to detect pieces
    time_interval = 0.3 #seconds
    while True:
        print(red, green, blue, yellow)

        #Trigger the start button if green piece is found
        if green >= 1 :
            if start == True:
                continue
            else:
                pp_button = browser.find_element_by_id('play-pause-button')
                pp_button.click()
                start = True            
        else:
            if start == True:
                pp_button = browser.find_element_by_id('play-pause-button')
                pp_button.click()
                start = False
            else:
                continue

        time.sleep(time_interval)




if __name__ == '__main__':
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
    pipeline.start(config)

    #Start threads
    try:
        _thread.start_new_thread(objectFound, (pipeline, ))
        _thread.start_new_thread(triggerFunc, ())
    except:
        print ("Error: unable to start thread")

    while True:
        pass
