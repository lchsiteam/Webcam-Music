import cv2
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,200,255,0)

    M = cv2.moments(thresh)

    try:
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])


        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    except:
        pass

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('picture',thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()