import cv2
import pyrealsense2 as rs
import svm_train as st
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
        #color_image = color_image[300:700, 300:500]

        cv2.imshow('Result', color_image)
        key = cv2.waitKey(10)
        if key == ord('s'):
            color_image = st.predict(color_image)

            cv2.imshow("Result", color_image)
            cv2.waitKey()
        if key == ord('e'):
            break




finally:
    pipeline.stop()
