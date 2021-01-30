from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle




class image :
    

    def image_read(self):
        #load the image
        self.im_read = imread("photo name")
        #load the pre-traind model
        self.classifier = CascadeClassifier('haarcascade_frontalface_default.xml')




    def face_detection(self):
        #print bounding box around face
        bboxes = self.classifier.detectMultiScale(self.im_read)
        for box in bboxes :
            x, y, width, height = box
            x2, y2 = x + width, y + height

            rectangle(self.im_read, (x,y), (x2, y2), (0,255,0), 1)
        



    def image_show(self):
        #show image after detect face
        imshow('Face Detection', self.im_read)
        waitKey(0) #wait any key to close window
        destroyAllWindows() #close window


s = image()
s.image_read()
s.face_detection()
s.image_show()
