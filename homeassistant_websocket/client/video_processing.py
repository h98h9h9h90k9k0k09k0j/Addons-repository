import cv2
import numpy as np
# Does processing on the received video data
# Should respond to the server depending on the type of processing

class VideoProcessor:
    @staticmethod
    async def process_video(message, websocket, clients):
        # Placeholder for video processing logic
        pass

    @staticmethod
    async def rt_face_recognition(message, websocket): #real time
        # Make sure to enable camera
        # Link to guide: https://towardsdatascience.com/real-time-face-recognition-an-end-to-end-project-b738bb0f7348
        faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml') #THERE MUST BE A CLASSIFIER INSIDE THIS FOLDER!
        cap = cv2.VideoCapture(0)
        while(True):
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(20, 20)
            )
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

            cv2.imshow('video',img)
    
            k = cv2.waitKey(30) & 0xff
            if k == 27: # press 'ESC' to quit
                break
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    async def motion_detection(video_source, message, websocket, clients):
        cap = cv2.VideoCapture(video_source)

        if not cap.isOpened():
            print("Error: Unable to open video source")
            return
        
        fgbg = cv2.createBackgroundSubtractorMOG2() #fgbg = foreground/background
        while True:
            ret, frame = cap.read()

            if not ret:
                break
            fgmask = fgbg.apply(frame) # apply background subtraction -> foreground mask image
            _, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY[1]) #colors above 200 turns white. [1] = thresholded image
            contours, hierarchy = cv2. findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #RETR_EXTERNAL = external contours, CHAIN... = compress to save memory
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #rectangle drawn around object if area is big enough
            cv2.imshow('frame', frame) #display frame

            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break #break loop with 'q'
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    async def motion_detected(video_source):
        cap = cv2.VideoCapture(video_source)

        if not cap.isOpened():
            print("Error: Unable to open video source")
            return
        
        fgbg = cv2.createBackgroundSubtractorMOG2() #fgbg = foreground/background
        while True:
            ret, frame = cap.read()

            if not ret:
                break
            fgmask = fgbg.apply(frame) # apply background subtraction -> foreground mask image
            _, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY[1]) #colors above 200 turns white. [1] = thresholded image
            contours, hierarchy = cv2. findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #RETR_EXTERNAL = external contours, CHAIN... = compress to save memory
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:
                    return True

        cap.release()
        cv2.destroyAllWindows()

        return False #not sure if necessary

    # Logic to send commands back to server depending on the processing
    @staticmethod
    async def send_command(message, websocket, clients):
        # Placeholder for sending commands back to server
        pass