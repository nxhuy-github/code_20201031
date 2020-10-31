import cv2

# Read image
img = cv2.imread('data/aero1.jpg', 1)

# Get image's shape
h, w, d = img.shape
print(h, w, d)
# print(img.reshape(3, 480, 640))

# BGR ordering
b, g, r = img[100, 50]
print(b,g,r)

# Show image
cv2.imshow('image', img)
#cv2.imshow('image reshape', img.reshape(3, 480, 640)) # -> error when run

# Slicing and Resizing image
roi = img[60:160, 50:150]
cv2.imshow('ROI', roi)
resized = cv2.resize(img, (200, 200)) # ignore aspect ratio
cv2.imshow('Resized', resized)
r = 200.0 / w
dim = (200, int(h * r)) # maintain aspect ratio
resized = cv2.resize(img, dim)
cv2.imshow("Aspect Ration", resized)

# Rotating image
center = w // 2, h // 2
rotation_matrix = cv2.getRotationMatrix2D(center, -45, 1)
rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
cv2.imshow('Rotated', rotated) # The image rotated will be clipped

# Blurring image
blurred = cv2.GaussianBlur(img, (11, 11), 0)
cv2.imshow('Blurred', blurred)

# Drawing on image
output = img.copy()
cv2.rectangle(output, (320, 60), (420, 160), (0, 0, 255), 2)
cv2.imshow('Rectangle', output)
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
cv2.imshow('Circle', output)
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
cv2.imshow('Line', output)
cv2.putText(output, 'OpenCV + Some city!!!', (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2)
cv2.imshow('Text', output)

cv2.waitKey(0) # click on image first and press a(any) key on the keyboard


