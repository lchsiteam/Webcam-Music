import cv2
import data
import builtins
import numpy as np

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

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,200,255,0)

        roiOut=thresh[0:cameraResolution[1], 0:cameraResolution[0]]
        roiLeft=thresh[0:cameraResolution[1], 0:cameraResolution[0]//3]
        roiRight=thresh[0:cameraResolution[1], cameraResolution[0]//3:cameraResolution[0]]

        MLeft = cv2.moments(roiLeft)
        MRight = cv2.moments(roiRight)
        
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
        cv2.imshow('frame',frame)
        cv2.imshow('mask',roiOut)
        if (cv2.waitKey(1) & 0xFF == 4 or not builtins.run):
            break

        outArray = [cameraResolution,leftcX,leftcY,rightcX,rightcY,scaleMode]
        params = handsToParams(outArray)
        volume, frequency, waveform = params

        data.frequency = frequency
        data.volume = volume
        data.waveform = waveform

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

    if not scaleMode:
        frequency = 523.252 - ( (rightY / screenHeight) * 261.625) 
    else:
        if rightY <= 1/13 * screenHeight:
            frequency = frequencyList[0]
        elif rightY <= 2/13 * screenWidth:
            frequency = frequencyList[1]
        elif rightY <= 3/13 * screenWidth:
            frequency = frequencyList[2]
        elif rightY <= 4/13 * screenWidth:
            frequency = frequencyList[3]
        elif rightY <= 5/13 * screenWidth:
            frequency = frequencyList[4]
        elif rightY <= 6/13 * screenWidth:
            frequency = frequencyList[5]
        elif rightY <= 7/13 * screenWidth:
            frequency = frequencyList[6]
        elif rightY <= 8/13 * screenWidth:
            frequency = frequencyList[7]
        elif rightY <= 9/13 * screenWidth:
            frequency = frequencyList[8]
        elif rightY <= 10/13 * screenWidth:
            frequency = frequencyList[9]
        elif rightY <= 11/13 * screenWidth:
            frequency = frequencyList[10]
        elif rightY <= 12/13 * screenWidth:
            frequency = frequencyList[11]
        else:
            frequency = frequencyList[12]

    selectedWaveForm = ''

    if rightX >= 7/9 * screenWidth:
        selectedWaveForm = Waveforms[2]
    elif rightX >= 5/9 * screenWidth:
        selectedWaveForm = Waveforms[1]
    else:
        selectedWaveForm = Waveforms[0]

    return [volume,frequency,selectedWaveForm]

# findHandPos(True)
