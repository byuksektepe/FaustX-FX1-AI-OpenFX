import cv2
import numpy as np

stability = 0.4

class ObjectDetection:
    def __init__(self, weights_path="dnn_models/yolov4-sm.weights", cfg_path="dnn_configs/yolov4-sm.cfg"):
        print("FaustX Object Tracking Loading...")
        print("Running opencv and nvidia cudnn")
        #Kararlılık Ayarı
        self.nmsThreshold = stability - 0.1
        self.confThreshold = stability
        self.image_size = 608

        # Load Network
        net = cv2.dnn.readNet(weights_path, cfg_path)

        # Enable GPU CUDA
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.model = cv2.dnn_DetectionModel(net)

        self.classes = []
        self.load_class_names()
        self.colors = np.random.uniform(0, 255, size=(80, 3))

        self.model.setInputParams(size=(self.image_size, self.image_size), scale=1/255)

    def load_class_names(self, classes_path="dnn_model/classes.txt"):

        with open(classes_path, "r") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()
                self.classes.append(class_name)

        self.colors = np.random.uniform(0, 255, size=(80, 3))
        return self.classes

    def detect(self, frame):
        return self.model.detect(frame, nmsThreshold=self.nmsThreshold, confThreshold=self.confThreshold)


    
class KalmanFilter:
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)


    def predict(self, coordX, coordY):
        measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        x, y = int(predicted[0]), int(predicted[1])
        return x, y
    
    def make_draw(self, img, cx, cy, color):
        
        predicted = self.predict(cx, cy)
        #cv2.circle(img, (predicted[0], predicted[1]), 10, (255, 0, 0), 2)
        #cv2.arrowedLine(img, (cx, cy),  (predicted[0], predicted[1]), color, 1, 8, 0, 0.1)
        cv2.circle(img, (cx, cy), 6, (0, 185, 255), 2, cv2.LINE_AA)
        cv2.circle(img, (predicted[0], predicted[1]), 6, color, 2, cv2.LINE_AA)
        
class BgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert Image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create a Mask with adaptive threshold
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.imshow("mask", mask)
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                #cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)

        return objects_contours

