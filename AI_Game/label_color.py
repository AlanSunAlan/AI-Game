import cv2
import pyrealsense2 as rs
import numpy as np
import file_manager as fm

#Function to save training samples
def save_sample(raw_img):
    result_x = []
    result_y = []
    #Get image size
    pLength_x = raw_img.shape[1]
    pLength_y = raw_img.shape[0]

    color_name = 'green'

    for pixel_x in range(0, pLength_x-1):
        for pixel_y in range(0, pLength_y-1):
            #Get the  bgr value of a single pixel
            b, g, r = raw_img[pixel_y, pixel_x]
            #print('R:%d; G:%d; B:%d') %(r,g,b)
            result_x.append([r, g, b])
            result_y.append(color_name)
            #save the array list to a file
            fm.save_labels(r, g, b, color_name)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
                continue

        # Convert realsense images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        roi = color_image[420:500, 590:660]

        cv2.imshow('Color Image', roi)
        key = cv2.waitKey(20)
        if key == ord('s'):
            save_sample(roi)
        elif key == ord('d'):
            continue
        elif key == ord('e'):
            break

finally:
    pipeline.stop()


