import svm_train as svm
import cv2

def color_name(circle_center, circle_radius, src_img):
    if not circle_center:
        return 'other'
    if not circle_radius:
        return 'other'
    #Create roi that only contains 
    blur_img = cv2.GaussianBlur(src_img, (5,5), 0)
    roi = createROI(blur_img, circle_center, circle_radius, 0.7)

    if not roi.any():
        return 'other'
    #Determine the main color of the roi
    #Take three samples
    #point1_xy = [int(circle_radius/2), int(circle_radius/2)]
    #point2_xy = [int(circle_radius/4), int(circle_radius/2)]
    #point3_xy = [int(3*circle_radius/4), int(circle_radius/2)]
    
    #b1, g1, r1 = roi[point1_xy[1], point1_xy[0]]
    #b2, g2, r2 = roi[point2_xy[1], point2_xy[0]]
    #b3, g3, r3 = roi[point3_xy[1], point3_xy[0]]

    #Predict the color of the three points
    #color1 = svm.predictRGB(r1, g1, b1)
    #color2 = svm.predictRGB(r2, g2, b2)
    #color3 = svm.predictRGB(r3, g3, b3)
    #print(color1, color2, color3)
    #If the color is the same, return it
    #if color1 == color2 and color2 == color3:
        #return color1
    #else:
        #return 'other'

    #Calculate the average rgb value of the center
    pLength_x = roi.shape[1]
    pLength_y = roi.shape[0]
    sum_r = 0
    sum_g = 0
    sum_b = 0
    count = 0
    for pixel_x in range(0, pLength_x-1):
        for pixel_y in range(0, pLength_y-1):
            b, g, r = roi[pixel_y, pixel_x]
            count = count + 1
            sum_r = sum_r + r
            sum_g = sum_g + g
            sum_b = sum_b + b

    avg_r = int(sum_r / count)
    avg_g = int(sum_g / count)
    avg_b = int(sum_b / count)

    return svm.predictRGB(avg_r, avg_g, avg_b)
    
        
def createROI(img_src, center, radius, scale):
    radius = scale * radius
    if len(center) == 2:
        rectCenter_x = center[0]
        rectCenter_y = center[1]
        start_x = int(rectCenter_x - radius)
        start_y = int(rectCenter_y - radius)
        end_x = int(rectCenter_x + radius)
        end_y = int(rectCenter_y + radius)
        img_result = img_src[start_y:end_y, start_x: end_x]

        result_center = [radius, radius]

        return img_result

    else:
        return []

#def ifInRange(roi, ):
