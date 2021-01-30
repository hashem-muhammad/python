import sys
import numpy as np
import time
import cv2
from requests_html import HTMLSession
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from WebScraping import WebScraping


from PyQt5.QtWidgets import QMainWindow,QInputDialog, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
from PyQt5 import QtCore,QtWidgets

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'WIU - H.B'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(60, 20)
        self.textbox.resize(280,40)
        # Create a button in the window
        self.button = QPushButton('Download photo', self)
        self.button.move(150,80)
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.button= QPushButton('Object detection', self)
        self.button.move(150,160)
        # connect button to function on_click
        self.button.clicked.connect(self.yes_click)
        self.show()
      #seleact files and choose image   
    def openFileNameDialog(self):
        global c 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            c=fileName

    @pyqtSlot()
    def on_click(self):
        global z
        z=self.textbox.text()
        url = z
        path = 'File Path'  
        WebScraping.main(url, path)
        

    #image name and object detection
    def yes_click(self):

        self.openFileNameDialog()
        self.show()
        INPUT_FILE=c
        OUTPUT_FILE='File Path'
        LABELS_FILE='File Path'
        CONFIG_FILE='File Path'
        WEIGHTS_FILE='File Path'
        CONFIDENCE_THRESHOLD=0.3

        LABELS = open(LABELS_FILE).read().strip().split("\n")

        np.random.seed(4)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
            dtype="uint8")


        net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)

        image = cv2.imread(INPUT_FILE)
        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()


        print("[INFO] YOLO took {:.6f} seconds".format(end - start))


        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > CONFIDENCE_THRESHOLD:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,
            CONFIDENCE_THRESHOLD)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in COLORS[classIDs[i]]]

                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

        # show the output image
        cv2.imshow("Resulte", image)
        cv2.waitKey(0)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())