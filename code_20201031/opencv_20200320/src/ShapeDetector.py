import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unidentified"
        # Calcul the perimeter of the contour
        peri = cv2.arcLength(c, True)
        # Contours approximation
        # Ramer-Douglas-Peucker algorithm
        approx = cv2.approxPolyDP(c, 0.04*peri, True)

        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            ar = w / float(h)

            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"
        return shape