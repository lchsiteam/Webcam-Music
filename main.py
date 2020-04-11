import cv2

def findHandPos (cameraResolution):
    cap = cv2.VideoCapture(1)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,200,255,0)

        roiLeft=thresh[0:cameraResolution[0]//3, 0:cameraResolution[1]]
        roiRight=thresh[0:cameraResolution[0]//3, cameraResolution[0]:cameraResolution[1]]

        MLeft = cv2.moments(roiLeft)
        MRight = cv2.moments(roiRight)

        
            # calculate x,y coordinate of center
        if (MLeft["m00"] != 0):
            cX = int(MLeft["m10"] / MLeft["m00"])
            cY = int(MLeft["m01"] / MLeft["m00"])


            cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(frame, "centroid Left", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        else:
            print(MLeft["m00"])
        

        try:
            # calculate x,y coordinate of center
            cX = int(MRight["m10"] / MRight["m00"])
            cY = int(MRight["m01"] / MRight["m00"])


            cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(frame, "centroid Right", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except:
            pass

        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.imshow('picture',roiLeft)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

findHandPos([1280,720])
