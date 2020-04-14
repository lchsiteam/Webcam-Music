import cv2
import numpy as np

class OpenCVVersionError(Exception): # for when there is incompatible version of opencv
    pass

MAJOR, MINOR, *_ = cv2.__version__.split('.') 

if MAJOR == '4': # opencv 4
    C_START = 0
elif MAJOR == '3': # opencv 3
    C_START = 1
else: # opencv not 3 or 4 and thus bad
    raise OpenCVVersionError(f'Your version of OpenCV ({cv2.__version__}) is incompatible; please upgrade to OpenCV 3 or OpenCV 4') 

#print(MAJOR) 

#make sure your hands are out of frame.  Do not move your head out of frame and then put it in, either always have it out, or always have it in
#press x
#move hands into respective boxes

x_size=float(1.0/3.0)  #represent 0.7ths of the screen (vertically divided)
y_size=1  #  (don't edit)
x1_max=0 #right hand x coor
x2_max=0 #left hand x coor
y1_max=719 #right hand y coor
y2_max=719 #left hand y coor
threshold = 60
isBgCaptured = 0

def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

camera = cv2.VideoCapture(0)

while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    frame=cv2.flip(frame,1)
    cv2.rectangle(frame, (int(x_size * frame.shape[1]), 0),
                 (frame.shape[1], int(y_size * frame.shape[0])), (255, 0, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
    cv2.rectangle(frame, (int((x_size-0.003) * frame.shape[1]), 0),
                 (0, int(y_size * frame.shape[0])), (0, 255, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
    cv2.imshow('original', frame)

    #  big boi calculations
    if isBgCaptured == 1:
        img = removeBG(frame)
        img1 = img[0:int(y_size * frame.shape[0]),
                     int(x_size * frame.shape[1]):frame.shape[1]]
        img2 = img[0:int(y_size * frame.shape[0]),
                     0:int(x_size * frame.shape[1])]

        # binary boi
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.GaussianBlur(gray1, (41, 41), 0) #<--blur boi 1
        blur2 = cv2.GaussianBlur(gray2, (41, 41), 0) #<--blur boi 2
        ret, thresh1 = cv2.threshold(blur1, threshold, 255, cv2.THRESH_BINARY)
        ret, thresh2 = cv2.threshold(blur2, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('ori 1', thresh1)
        cv2.imshow('ori 2', thresh2)

        #_, contours, _= cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        '''
        _, contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        _, contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ''' 
        
        c = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        c2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

        contours1, hierarchy1 = c[C_START:] 
        contours2, hierarchy2 = c2[C_START:] 

        length1 = len(contours1)
        length2 = len(contours2)
        maxArea = -1
        if length1 > 0:
            for i in range(length1):
                temp = contours1[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
            res = contours1[ci]
            y1_max = 719
            for i in range(len(res)):
                res[i][0][0]+=(frame.shape[1]/3.0)
                if res[i][0][1] < y1_max:
                    y1_max = res[i][0][1]
                    x1_max = res[i][0][0]
            cv2.drawContours(frame, [res], 0, (0, 255, 0), 2)
            cv2.circle(frame, (x1_max, y1_max), 3, (0, 0, 255), 3)

        maxArea = -1
        if length2 > 0:
            for i in range(length2):
                temp = contours2[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
            res = contours2[ci]
            y2_max = 719
            for i in range(len(res)):
                if res[i][0][1] < y2_max:
                    y2_max = res[i][0][1]
                    x2_max = res[i][0][0]
            cv2.drawContours(frame, [res], 0, (0, 255, 0), 2)
            cv2.circle(frame, (x2_max, y2_max), 3, (0, 0, 255), 3)

        cv2.imshow('original', frame)

        #res is the list of countours points
        #x2_max, x1_max, y2_max, and y1_max are the fingertip coordinates.
        #(x2,y2) is left hand, (x1,y1) is right hand

    k = cv2.waitKey(10)
    if k == 27:
        camera.release() #exits
        cv2.destroyAllWindows()
        print('yeet', res[0][0][0])
        print(res.max())
        break
    elif k == ord('x'):  #press x to doubt, and to capture background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
        isBgCaptured = 1
