import cv2
import numpy as np
import pyrealsense2 as rs

def find_circles(raw_image):
    result_center = []
    result_radius = []
    
    default_hough = load_default()

    if raw_image is not None:
        circles = []
        #Pre-processing
        b, g, r = cv2.split(raw_image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        b = clahe.apply(b)
        g = clahe.apply(g)
        r = clahe.apply(r)
        raw_image = cv2.merge([b,g,r])
        img_gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

        if len(default_hough) == 4:
            circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=default_hough[0],param2=default_hough[1],
                            minRadius=default_hough[2],maxRadius=default_hough[3])
        else:
            circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20,
                                    param1=50,param2=30,minRadius=5,maxRadius=20)

    try:
        circles = np.uint16(np.around(circles))
    except:
        #print('[Circles can not be find using Hough Transformation]')
        #cv2.imshow('Circle Detection Result', raw_image)
        #cv2.waitKey(20)
        return result_center, result_radius

    for i in circles[0,:]:
        # draw the outer circle
        #cv2.circle(raw_image,(i[0],i[1]),i[2],(0,255,0),1)
        # draw the center of the circle
        #cv2.circle(raw_image,(i[0],i[1]),2,(0,0,255),1)
        # apend radius, centers
        center = [i[0], i[1]]
        radius = i[2]
        result_center.append(center)
        result_radius.append(radius)

    #cv2.imshow('Circle Detection Result', raw_image)
    #cv2.waitKey(20)
    return result_center, result_radius

def load_default():
    #Create a list to store parameter values, and read default value
    default_hough = []
    #Read the file line by line
    f = open('./config/hough.config', 'r')
    line = f.readline()
    while line:
        value = int(line)
        default_hough.append(value)
        line = f.readline()
    f.close()
    return default_hough

def save_value(pos):
    #Save the value to the file
    fname = './config/hough.config'
    info_file = open(fname, 'w+')

    #Get current trackbar position
    param1 = cv2.getTrackbarPos('Param1', 'Hough Parameters')
    param2 = cv2.getTrackbarPos('Param2', 'Hough Parameters')
    minRadius = cv2.getTrackbarPos('Minimum radius', 'Hough Parameters')
    maxRadius = cv2.getTrackbarPos('Maximum radius', 'Hough Parameters')

    info_file.write(str(param1) + '\n')
    info_file.write(str(param2) + '\n')
    info_file.write(str(minRadius) + '\n')
    info_file.write(str(maxRadius) + '\n')

if __name__ == '__main__':
    #Start streaming
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
    pipeline.start(config)

    default_hough = load_default()

    #Create trackbars
    cv2.namedWindow('Hough Parameters')
    if len(default_hough) == 4:
        param1_bar = cv2.createTrackbar('Param1', 'Hough Parameters', default_hough[0], 100, save_value)
        param2_bar = cv2.createTrackbar('Param2', 'Hough Parameters', default_hough[1], 100, save_value)
        minR_bar = cv2.createTrackbar('Minimum radius', 'Hough Parameters', default_hough[2], 200, save_value)
        maxR_bar = cv2.createTrackbar('Maximum radius', 'Hough Parameters', default_hough[3], 200, save_value)
        clip_bar = cv2.createTrackbar('clipLimit', 'Hough Parameters', 2, 50, save_value)
        tile_bar = cv2.createTrackbar('Tile Grid Size', 'Hough Parameters', 8, 30, save_value)
    else:
        param1_bar = cv2.createTrackbar('Param1', 'Hough Parameters', 50, 200, save_value)
        param2_bar = cv2.createTrackbar('Param2', 'Hough Parameters', 30, 200, save_value)
        minR_bar = cv2.createTrackbar('Minimum radius', 'Hough Parameters', 10, 200, save_value)
        maxR_bar = cv2.createTrackbar('Maximum radius', 'Hough Parameters', 30, 200, save_value)
        clip_bar = cv2.createTrackbar('clipLimit', 'Hough Parameters', 2, 50, save_value)
        tile_bar = cv2.createTrackbar('Tile Grid Size', 'Hough Parameters', 8, 30, save_value)
    
    #Create window to show stream
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('Test Window', cv2.WINDOW_AUTOSIZE)

    #Start testing parameters
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert realsense images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            roi = color_image
            #[500:1000, 500: 1000]
        
            #Pre-processing
            clipLmt = cv2.getTrackbarPos('clipLimit','Hough Parameters')
            tileSize = cv2.getTrackbarPos('Tile Grid Size','Hough Parameters')
            roi = cv2.bilateralFilter(roi,5,30,30)
            b, g, r = cv2.split(roi)
            clahe = cv2.createCLAHE(clipLimit=clipLmt, tileGridSize=(tileSize,tileSize))
            b = clahe.apply(b)
            g = clahe.apply(g)
            r = clahe.apply(r)
            roi = cv2.merge([b,g,r])
            roi = cv2.bilateralFilter(roi,3,20,30)
            img_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            #img_equal = cv2.equalizeHist(img_gray)

            #Detect circles
            param1 = cv2.getTrackbarPos('Param1', 'Hough Parameters')
            param2 = cv2.getTrackbarPos('Param2', 'Hough Parameters')
            minRadius = cv2.getTrackbarPos('Minimum radius', 'Hough Parameters')
            maxRadius = cv2.getTrackbarPos('Maximum radius', 'Hough Parameters')
            circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20,
                                param1=param1,param2=param2,minRadius=minRadius,maxRadius=maxRadius)

            try:
                circles = np.uint16(np.around(circles))
            except AttributeError as e:
                print(e)
                print('[Circles can not be find using Hough Transformation]')
                cv2.imshow('RealSense', roi)
                cv2.waitKey(20)
                continue

            print('Circles found, drawing circles')
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(roi,(i[0],i[1]),i[2],(0,255,0),1)
                # draw the center of the circle
                cv2.circle(roi,(i[0],i[1]),2,(0,0,255),1)

            # Show images
            cv2.imshow('RealSense', roi)
            cv2.imshow('Pre-processing', img_gray)
            cv2.waitKey(50)

    finally:
        pipeline.stop()
