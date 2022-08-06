import cv2
import numpy as np


class KalmanFilter:
    def __init__(self):
        pass

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
        # cv2.circle(img, (predicted[0], predicted[1]), 10, (255, 0, 0), 2)
        # cv2.arrowedLine(img, (cx, cy),  (predicted[0], predicted[1]), color, 1, 8, 0, 0.1)
        cv2.circle(img, (cx, cy), 6, (0, 185, 255), 2, cv2.LINE_AA)
        cv2.circle(img, (predicted[0], predicted[1]), 6, color, 2, cv2.LINE_AA)