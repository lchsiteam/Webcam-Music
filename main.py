import cv2
import data
import builtins
import numpy as np

builtins.captureBackground = False
builtins.run = True

def removeBG(frame):
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
        threshold = 60

        # Capture frame-by-frame
        ret, frame = cap.read()

        '''
        frame=cv2.flip(frame,1)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,200,255,0)
        '''

        frame = cv2.bilateralFilter(frame, 5, 50, 100)
        frame=cv2.flip(frame,1)
        cv2.rectangle(frame, (int(x_size * frame.shape[1]), 0),
                    (frame.shape[1], int(y_size * frame.shape[0])), (255, 0, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        cv2.rectangle(frame, (int((x_size-0.003) * frame.shape[1]), 0),
                    (0, int(y_size * frame.shape[0])), (0, 255, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        cv2.imshow('original', frame)

        #  big boi calculations
        
        if builtins.captureBackground:
            bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
            builtins.captureBackground = False
            
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
            blur3 = cv2.GaussianBlur(gray3, (41, 41), 0) #<--blur boi 3
            ret, thresh1 = cv2.threshold(blur1, threshold, 255, cv2.THRESH_BINARY)
            ret, thresh2 = cv2.threshold(blur2, threshold, 255, cv2.THRESH_BINARY)
            ret, thresh3 = cv2.threshold(blur3, threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('ori1', thresh3)

            MLeft = cv2.moments(thresh2)
            MRight = cv2.moments(thresh1)
            
                # calculate x,y coordinate of center
            if (MLeft["m00"] != 0):
                leftcX = int(MLeft["m10"] / MLeft["m00"])
                leftcY = int(MLeft["m01"] / MLeft["m00"])


                cv2.circle(frame, (leftcX, leftcY), 5, (255, 255, 255), -1)
                cv2.putText(frame, "centroid Left", (leftcX - 25, leftcY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            else:
                leftcX = -1
                leftcY = -1

            if (MRight["m00"] != 0):
                # calculate x,y coordinate of center
                rightcX = int(MRight["m10"] / MRight["m00"])
                rightcY = int(MRight["m01"] / MRight["m00"])

                rightcX += cameraResolution[0]//3


                cv2.circle(frame, (rightcX, rightcY), 5, (255, 255, 255), -1)
                cv2.putText(frame, "centroid Right", (rightcX - 25, rightcY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            else:
                rightcX = -1
                rightcY = -1

            # Display the resulting frame
            #cv2.imshow('frame',frame)
            #cv2.imshow('mask',img)
            

            outArray = [cameraResolution,leftcX,leftcY,rightcX,rightcY,scaleMode]
            params = handsToParams(outArray)
            volume, frequency, waveform = params

            data.frequency = frequency
            data.volume = volume
            data.waveform = waveform

            print("updated")

            

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
