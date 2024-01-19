import cv2
import math

image = cv2.imread("blank.jpg")

cv2.namedWindow("image")
cv2.namedWindow("result")
pressed = False

h, w, _= image.shape
lastpoint = None
stay = True

def draw(blacks, slopes):
    current = 100
    a = len(blacks)
    global image
    result = image
    for i in range(h):
        for j in range(w):
            if (i, j) not in blacks:
                value = 0
                for bn in range(a):
                    x = blacks[bn]
                    rsquared = (x[0] - i)**2 + (x[1] - j)**2
                    if (x[1] - j) != 0:
                        rsloped = math.atan((x[0] - i)/(x[1] - j))
                    else:
                        rsloped = math.pi/2
                    
                    cross = math.sin(slopes[bn] - rsloped)
                    value += (current * cross)/rsquared
                if int(50 * abs(value)) <= 255:
                    if value > 0:
                        result[i, j] = (int(50 * value), 0, 0)
                    elif value < 0:
                        result[i, j] = (0, 0, int(50 * (-value)))                    
                else:
                    if value > 0:
                        result[i, j] = (255, 0, 0)
                    elif value < 0:
                        result[i, j] = (0, 0, 255)

    cv2.imshow("result", result)
slopes = []
blacks = []
def drag(event, x, y, flags, param):
    global pressed
    global lastpoint
    global slopes
    global blacks
    
    if x > w - 100 and x < w and y > h - 50 and y < h:
        if event == cv2.EVENT_MOUSEMOVE:
            cv2.rectangle(image, (w-100, h - 50), (w, h), (100, 100, 100), -1)
        elif event == cv2.EVENT_LBUTTONDOWN:
            cv2.rectangle(image, (w-100, h - 50), (w, h), (100, 0, 0), -1)
            draw(blacks, slopes)
            
    else:
        cv2.rectangle(image, (w-100, h - 50), (w, h), (200, 200, 200), -1)
        if pressed and event == cv2.EVENT_MOUSEMOVE and x < w and y < h:
            if lastpoint:
                cv2.line(image, lastpoint, (x, y), (0, 0, 0), 1)
                if lastpoint[0] - x != 0:
                    slope = (lastpoint[1] - y)/(lastpoint[0] - x)
                    slopes.append(math.atan(slope))
                else:
                    slopes.append(math.pi/2)
                blacks.append(((lastpoint[1] + y)/2, (lastpoint[0] + x)/2))
                lastpoint = (x, y)
            else:
                lastpoint = (x, y)
                
        if not pressed and event == cv2.EVENT_LBUTTONDOWN:
            pressed = True
        elif event == cv2.EVENT_LBUTTONUP:
            pressed = False
    
        
cv2.setMouseCallback("image", drag)

while stay:
    cv2.imshow("image", image)
    cv2.waitKey(1)
