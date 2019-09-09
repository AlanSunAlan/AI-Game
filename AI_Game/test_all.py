import circle_detector as cid
import color_detector as cod
import cv2
import pyrealsense2 as rs
import numpy as np

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert realsense images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        img_draw = color_image.copy()

        ccenters, cradius = cid.find_circles(color_image)

        for i in range(len(ccenters)):
            color = cod.color_name(ccenters[i], cradius[i], color_image)
            if color == 'red':
                cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (0, 90, 255), 3)
            if color == 'green':
                cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (90, 255, 0), 3)
            if color == 'blue':
                cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (255, 100, 0), 3)
            if color == 'yellow':
                cv2.circle(img_draw, (ccenters[i][0], ccenters[i][1]), 2, (0, 200, 255), 3)

        cv2.imshow('Detection Result', img_draw)
        cv2.waitKey(1)
    
finally:
    pipeline.stop()