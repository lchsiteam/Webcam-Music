import cv2
import data
import builtins
import numpy as np

#1) make sure your hands are out of frame.  Do not move your head out of frame and then put it back in, either always have it out, or always have it in.
#2) press x
#3) move hands into respective boxes

data.captureBackground = False
data.run = True
data.currentOctive = 2

x_size=float(1.0/3.0)  #represent 0.7ths of the screen (vertically divided)
y_size=1  #  (don't edit)
x1_max=0 #right hand x coor
x2_max=0 #left hand x coor
y1_max=719 #right hand y coor
y2_max=719 #left hand y coor
threshold = 60 #no change needed in most situations

def findHandPos (scaleMode):
    cap = cv2.VideoCapture(0)
    cameraResolution = [int(cap.get(3)), int(cap.get(4))]
    bgModel = -1
    
    isBgCaptured = 0

    while True:

        # Capture frame-by-frame
        '''
        frame=cv2.flip(frame,1)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,200,255,0)
        '''

        ret, frame = cap.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)
        frame=cv2.flip(frame,1) #mirror webcam
        #draw rectange frame for right hand
        cv2.rectangle(frame, (int(x_size * frame.shape[1]), 0),
                    (frame.shape[1], int(y_size * frame.shape[0])), (255, 0, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        #draw rectange frame for left hand
        cv2.rectangle(frame, (int((x_size-0.003) * frame.shape[1]), 0),
                    (0, int(y_size * frame.shape[0])), (0, 255, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        #cv2.line(frame,(int(x_size * frame.shape[1]), 0),(int(x_size * frame.shape[1]), int(y_size * frame.shape[0])),(0, 0, 0), 5)

        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(frame,'Left Hand',(frame.shape[1]//20,20),font,1,(255,140,140),1)
        cv2.putText(frame,'Right Hand',(frame.shape[0]//20*15,20),font,1,(255,140,140),1)
        cv2.putText(frame,'On',(frame.shape[1]//40*36,frame.shape[0]//40*4),font,1,(255,140,140),1)
        cv2.putText(frame,'Off',(frame.shape[1]//40*35,frame.shape[0]//40*37),font,1,(255,140,140),1)


        cv2.line(frame,(frame.shape[1]//40,frame.shape[0]//20),(frame.shape[1]//40,frame.shape[0]//20*19),(40,40,240),2) #volume Line, Left side of the screen
        cv2.line(frame,(frame.shape[1]//40*39,frame.shape[0]//40),(frame.shape[1]//40*39,frame.shape[0]//3*2),(40,240,40),2) #On Line, right side of the screen, green
        cv2.line(frame,(frame.shape[1]//40*39,frame.shape[0]//3*2),(frame.shape[1]//40*39,frame.shape[0]//20*19),(40,40,240),2) #Off Line, right side of the screen, red, bottom

        cv2.line(frame,(frame.shape[1]//36 ,frame.shape[0]//40*39),(frame.shape[1]//9,frame.shape[0]//40*39),(40,240,40),3) #Square Line, left side of the screen, Green
        cv2.line(frame,(frame.shape[1]//9 ,frame.shape[0]//40*39),(frame.shape[1]//9*2,frame.shape[0]//40*39),(40,240,240),3) #Triangle Line, left side of the screen, Yellow, 
        cv2.line(frame,(frame.shape[1]//9*2 ,frame.shape[0]//40*39),(frame.shape[1]//108*40,frame.shape[0]//40*39),(240,40,40),3) #Sine Line, left side of the screen, Bule,

        cv2.line(frame,(int(frame.shape[1]//19.5*6 +frame.shape[0]//19),frame.shape[0]//40*39),(int(frame.shape[1]//19.5*7+frame.shape[0]//19),frame.shape[0]//40*39),(31,63,246),3) #The 13 pitches at the bottom
        cv2.line(frame,(int(frame.shape[1]//19.5*7 +frame.shape[0]//19),frame.shape[0]//40*39),(int(frame.shape[1]//19.5*8+frame.shape[0]//19),frame.shape[0]//40*39),(14,198,160),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*8 +frame.shape[0]//19),frame.shape[0]//40*39),(int(frame.shape[1]//19.5*9+frame.shape[0]//19),frame.shape[0]//40*39),(40,40,40),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*9 +frame.shape[0]//19),frame.shape[0]//40*39),(int(frame.shape[1]//19.5*10+frame.shape[0]//19),frame.shape[0]//40*39),(207,122,77),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*10+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*11+frame.shape[0]//19),frame.shape[0]//40*39),(40,40,40),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*11+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*12+frame.shape[0]//19),frame.shape[0]//40*39),(1,166,252),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*12+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*13+frame.shape[0]//19),frame.shape[0]//40*39),(172,98,173),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*13+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*14+frame.shape[0]//19),frame.shape[0]//40*39),(40,40,40),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*14+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*15+frame.shape[0]//19),frame.shape[0]//40*39),(1,235,255),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*15+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*16+frame.shape[0]//19),frame.shape[0]//40*39),(40,40,40),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*16+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*17+frame.shape[0]//19),frame.shape[0]//40*39),(172,181,17),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*17+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*18+frame.shape[0]//19),frame.shape[0]//40*39),(40,40,40),3) 
        cv2.line(frame,(int(frame.shape[1]//19.5*18+frame.shape[0]//19) ,frame.shape[0]//40*39),(int(frame.shape[1]//19.5*19+frame.shape[0]//19),frame.shape[0]//40*39),(31,63,246),3) 
     

        cv2.imshow('original', frame)

        
        cv2.imshow('original', frame)

        if data.captureBackground:
            bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
            data.captureBackground = False

        #  big boi calculations
        if bgModel != -1:
            fgmask = bgModel.apply(frame,learningRate=0)
            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            img = cv2.bitwise_and(frame, frame, mask=fgmask)
            #layout rectangular boundaries for each hand
            img1 = img[0:int(y_size * frame.shape[0]),
                        int(x_size * frame.shape[1]):frame.shape[1]]
            img2 = img[0:int(y_size * frame.shape[0]),
                        0:int(x_size * frame.shape[1])]
            
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            gray3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur1 = cv2.GaussianBlur(gray1, (41, 41), 0) #<--blur boi 1
            blur2 = cv2.GaussianBlur(gray2, (41, 41), 0) #<--blur boi 2
            blur3 = cv2.GaussianBlur(gray3, (41, 41), 0) #<--blur boi 3 (combined 1 and 2)
            ret, thresh1 = cv2.threshold(blur1, threshold, 255, cv2.THRESH_BINARY)
            ret, thresh2 = cv2.threshold(blur2, threshold, 255, cv2.THRESH_BINARY)
            ret, thresh3 = cv2.threshold(blur3, threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('Mask', thresh3)

            # once B&W image is created, find Countours
            contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length1 = len(contours1)
            length2 = len(contours2)
            maxArea = -1
            if length1 > 0:
                for i in range(length1): #find contour area
                    temp = contours1[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i
                res = contours1[ci]
                y1_max = frame.shape[0]-1
                for i in range(len(res)): #adjust offset on right hand + get top of hand coordinates
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
                    y2_max = frame.shape[0]-1
                    for i in range(len(res)): # get top of hand coordinates for left hand
                        if res[i][0][1] < y2_max:
                            y2_max = res[i][0][1]
                            x2_max = res[i][0][0]
                    cv2.drawContours(frame, [res], 0, (0, 255, 0), 2) #draw contours
                    cv2.circle(frame, (x2_max, y2_max), 3, (0, 0, 255), 3) #draw top of hands

                cv2.circle(frame,(frame.shape[1]//40,y2_max),4,(240,40,40),4) #volume dot
                cv2.circle(frame,(frame.shape[1]*39//40,y1_max),4,(240,40,40),4) #On/Off dot
                cv2.circle(frame, (x2_max, frame.shape[0]//40*39), 4, (240, 40, 40), 4) #waveform dot
                cv2.circle(frame, (x1_max, frame.shape[0]//40*39), 4, (240, 40, 40), 4) #pitch dot

                cv2.imshow('original', frame) #draw frame
                    

                # Display the resulting frame
                #cv2.imshow('frame',frame)
                #cv2.imshow('mask',img)

                outArray = [cameraResolution,x2_max,y2_max,x1_max,y1_max,scaleMode,data.currentOctive]
                params = handsToParams(outArray)
                volume, frequency, waveform = params

                data.frequency = frequency
                data.volume = volume
                data.waveform = waveform

        if (cv2.waitKey(1) & 0xFF == 4 or not data.run):
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
    octave = inputArray[6]
    
    
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
        frequency =  ( ( (rightX - rightSideSupplement) / rightSideWidth) *  261.625) +  261.625

    else:
        if rightX <= 1/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[12]
        elif rightX <= 2/13 * rightSideWidth + rightSideSupplement :
            frequency = frequencyList[11]
        elif rightX <= 3/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[10]
        elif rightX <= 4/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[9]
        elif rightX <= 5/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[8]
        elif rightX <= 6/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[7]
        elif rightX <= 7/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[6]
        elif rightX <= 8/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[5]
        elif rightX <= 9/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[4]
        elif rightX <= 10/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[3]
        elif rightX <= 11/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[2]
        elif rightX <= 12/13 * rightSideWidth + rightSideSupplement:
            frequency = frequencyList[1]
        else:
            frequency = frequencyList[0]
            
    if octave == 1:
        frequency /= 2
    elif octave == 3:
        frequency *= 2
  

    return [volume,frequency,selectedWaveForm]

# findHandPos(True)
