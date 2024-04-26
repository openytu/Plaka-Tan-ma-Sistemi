import cv2 
from ultralytics import YOLO 
import imutils 
import numpy as np
import argparse
import easyocr 

# Constructing the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", default="models/license_plate_detector.pt", help="Path to YOLO model file (.onnx or .pt)")
ap.add_argument("-s", "--source", default="resimler/plate_2.jpg", help="Path to input image file")
args = vars(ap.parse_args())

##################

img = cv2.imread(args["source"])
model = YOLO(args["model"])

##################

thickness = 2
font = cv2.FONT_HERSHEY_PLAIN
font_scale = 0.8
threshold = 0.3

reader = easyocr.Reader(['en'], gpu=False)


img = imutils.resize(img, width=600)
results = model.track(img, persist=True, verbose = False)[0]
bboxes = np.array(results.boxes.data.tolist(), dtype = "int")

for box in bboxes:
        
    x1, y1, x2, y2, track_id, score, class_id = box
    img_roi = img[y1:y2, x1:x2]
    text_detections = reader.readtext(img_roi)
    
    for boxes, text, score_text in text_detections:
        print(text)
        text = "ID: {}  PLATE: {}".format(track_id, text)
        cv2.putText(img, text, (x1, y1 -5), font, font_scale, (0,255,0), thickness, cv2.LINE_AA)
        cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0), thickness)
        cv2.imshow("img",img)


cv2.waitKey(0)
cv2.destroyAllWindows()