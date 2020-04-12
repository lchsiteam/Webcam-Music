import cv2
import data
import builtins
import numpy as np

builtins.captureBackground = False
builtins.run = True

def removeBG(frame):   #removes the background from the input frame
    fgmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

def findHandPos (scaleMode):
    cap = cv2.VideoCapture(0)
    cameraResolution = [int(cap.get(3)), int(cap.get(4))]
    bgModel = -1
    

    while True:
        x_size=float(1.0/3.0)  #represent 0.7ths of the screen (vertically divided)
        y_size=1  #  (don't edit)
        x1_max=0 #right hand x coor
        x2_max=0 #left hand x coor
        y1_max=719 #right hand y coor
        y2_max=719 #left hand y coor
        threshold = 60
        isBgCaptured = 0

        
        # Capture frame-by-frame
        

        '''
        frame=cv2.flip(frame,1)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,200,255,0)
        '''

        ret, frame = cap.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)
        frame=cv2.flip(frame,1)
        cv2.rectangle(frame, (int(x_size * frame.shape[1]), 0),
                    (frame.shape[1], int(y_size * frame.shape[0])), (255, 0, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        cv2.rectangle(frame, (int((x_size-0.003) * frame.shape[1]), 0),
                    (0, int(y_size * frame.shape[0])), (0, 255, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        cv2.imshow('original', frame)

        if builtins.captureBackground:
            bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
            builtins.captureBackground = False

        #  big boi calculations
        if bgModel != -1:
            fgmask = bgModel.apply(frame,learningRate=0)
            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            img = cv2.bitwise_and(frame, frame, mask=fgmask)
            
            img1 = img[0:int(y_size * frame.shape[0]),
                        int(x_size * frame.shape[1]):frame.shape[1]]
            img2 = img[0:int(y_size * frame.shape[0]),
                        0:int(x_size * frame.shape[1])]

            # binary boi
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            gray3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur1 = cv2.GaussianBlur(gray1, (41, 41), 0) #<--blur boi 1
            blur2 = cv2.GaussianBlur(gray2, (41, 41), 0) #<--blur boi 2
            blur3 = cv2.GaussianBlur(gray3, (41, 41), 0) #<--blur boi 2
            ret, thresh1 = cv2.threshold(blur1, threshold, 255, cv2.THRESH_BINARY)
            ret, thresh2 = cv2.threshold(blur2, threshold, 255, cv2.THRESH_BINARY)
            ret, thresh3 = cv2.threshold(blur3, threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('Mask', thresh3)

            contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
                    

                # Display the resulting frame
                #cv2.imshow('frame',frame)
                #cv2.imshow('mask',img)

                outArray = [cameraResolution,x2_max,y2_max,x1_max,y1_max,scaleMode]
                params = handsToParams(outArray)
                volume, frequency, waveform = params

                data.frequency = frequency
                data.volume = volume
                data.waveform = waveform

        if (cv2.waitKey(1) & 0xFF == 4 or not builtins.run):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def handsToParams(inputArray):
    Waveforms = ['Sin','Triangle','Square']


    screenWidth = inputArray[0][0]
    screenHeight = inputArray[0][1]
    leftX = inputArray[1]
    leftY = inputArray[2]
    rightX = inputArray[3]
    rightY = inputArray[4]
    scaleMode = inputArray[5]

    frequencyList = [523.251, 493.883, 466.164, 440, 415.305, 391.995, 369.994, 349.228, 329.628, 311.127, 293.665, 277.183, 261.626]
    #  c5, b4, a#4, a4, g#4, g4 f#4 f4 e4 d#4 d4 c#4 c4

    volume = 100 - ( (leftY / screenHeight) * 100)




    selectedWaveForm = ''

    if leftX <= 1/9 * screenWidth:
        selectedWaveForm = Waveforms[2]
    elif leftX <= 2/9 * screenWidth:
        selectedWaveForm = Waveforms[1]
    else:
        selectedWaveForm = Waveforms[0]



    rightSideHeight = screenHeight * (2/3)
    rightSideWidth = screenWidth * (2/3)
    rightSideSupplement =screenWidth * (1/3)

    if rightY >= (rightSideHeight):
        volume = 0


    if not scaleMode:
        frequency = ( ( (rightX - rightSideSupplement) / rightSideWidth) * 261.625) + 261.625

    else:
        if rightX <= 1/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[0]
        elif rightX <= 2/13 * rightSideWidth + rightSideSupplement :
            frequency = frequencyList[1]
        elif rightX <= 3/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[2]
        elif rightX <= 4/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[3]
        elif rightX <= 5/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[4]
        elif rightX <= 6/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[5]
        elif rightX <= 7/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[6]
        elif rightX <= 8/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[7]
        elif rightX <= 9/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[8]
        elif rightX <= 10/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[9]
        elif rightX <= 11/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[10]
        elif rightX <= 12/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[11]
        else:
            frequency = frequencyList[12]

    return [volume,frequency,selectedWaveForm]

# findHandPos(True)
