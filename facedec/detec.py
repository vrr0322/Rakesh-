#Install opencv -python for import cv2,glob.
import cv2,glob

#glob is a path recogniser to get all the images in this folder "*.jpg" format.
allimages=glob.glob("*.jpg")

#haarcascade xml file to detect all faces.
detect=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#collecting images one by one.
for images in allimages:
    image=cv2.imread(images)
#converting image into gray image.
    gray_img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#get all face points.
    face_axis=detect.detectMultiScale(gray_img,1.5,5)

    for (x,y,w,h) in face_axis:
        final_image=cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
#show image.    
    cv2.imshow("Face Detected",image)
#wait key 0 wait until we close or make display  with milliseconds.
    cv2.waitKey(0)
#close the window.
    cv2.destroyAllWindows()
        
