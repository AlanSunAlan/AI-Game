from sklearn import svm
from joblib import dump, load
import file_manager as fm
import cv2

def train():
    X, Y = fm.read_label()
    clf = svm.SVC(gamma='scale')
    clf.fit(X, Y)

    dump(clf, './config/svm_color.joblib') 

def predict(src_img):
    X, Y = fm.read_label()
    clf = svm.SVC(gamma='scale')
    clf.fit(X, Y)

    pLength_x = src_img.shape[1]
    pLength_y = src_img.shape[0]

    image = src_img.copy()

    for pixel_x in range(0, pLength_x-1):
        for pixel_y in range(0, pLength_y-1):
            b, g, r = image[pixel_y, pixel_x]
            print(r, g, b)
            prediction = clf.predict([[r, g, b]])
            print(prediction)
            #print('Result: %s RGB: [%d, %d, %d]') %(prediction, r, g, b)
            if prediction == 'red':
                cv2.circle(src_img, (pixel_x, pixel_y), 1, (0, 0, 255), -1)
            elif prediction == 'blue':
                cv2.circle(src_img, (pixel_x, pixel_y), 1, (255, 0, 0), -1)
            elif prediction == 'yellow':
                cv2.circle(src_img, (pixel_x, pixel_y), 1, (0, 250, 255), -1)
            elif prediction == 'green':
                cv2.circle(src_img, (pixel_x, pixel_y), 1, (0, 255, 0), -1)
    return src_img

def predictRGB(r, g, b):
    clf = load('./config/svm_color.joblib') 

    return clf.predict([[r, g, b]])

#cv2.imread()


if __name__ == '__main__':
    train()
    print('Test Color (255, 30, 50), result: ', predictRGB(255, 30, 50))


            