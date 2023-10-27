import numpy as np
import cv2
# Read from the first camera device
cap = cv2.VideoCapture(0)

topLeft = (50, 50)
bottomRight = (300, 300)

bold = 0
bold1=0 
bold2=0
bold3=0
bold4=0
bold5=0
bold6=0
# Callback function for the trackbar
def on_bold_trackbar(value):
    #print("Trackbar value:", value)
    global bold
    bold = value

def on_bold_trackbar1(value):
    #print("Trackbar value:", value)
    global bold1
    bold1 = value
def on_bold_trackbar2(value):
    #print("Trackbar value:", value)
    global bold2
    bold2 = value
def on_bold_trackbar3(value):
    #print("Trackbar value:", value)
    global bold3
    bold3 = value
def on_bold_trackbar4(value):
    #print("Trackbar value:", value)
    global bold4
    bold4 = value

def on_bold_trackbar5(value):
    #print("Trackbar value:", value)
    global bold5
    bold5 = value
def on_bold_trackbar6(value):
    #print("Trackbar value:", value)
    global bold6
    bold6 = value

cv2.namedWindow("Camera")
cv2.createTrackbar("thin", "Camera", bold,10 , on_bold_trackbar)
cv2.createTrackbar("size", "Camera", bold1,10 , on_bold_trackbar1)
cv2.createTrackbar("blue", "Camera", bold2,254 , on_bold_trackbar2)
cv2.createTrackbar("green", "Camera", bold3,254 , on_bold_trackbar3)
cv2.createTrackbar("red", "Camera", bold4,254 , on_bold_trackbar4)
cv2.createTrackbar("x point", "Camera", bold5,700 , on_bold_trackbar5)
cv2.createTrackbar("y point", "Camera", bold6,500 , on_bold_trackbar6)
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(param, (x,y), 5, (0, 0, 255), 5)
        cv2.imshow("Camera",frame)

# 성공적으로 video device 가 열렸으면 while 문 반복
while(cap.isOpened()):
    # 한 프레임을 읽어옴
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Line
    cv2.line(frame, topLeft, bottomRight, (0, 255, 0), 5)

    # Text 
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "ME",(50+bold5,100+bold6) , cv2.FONT_ITALIC, 1+bold1, (0+bold2, 0+bold3, 0+bold4), 1 + bold)

    # Display
    cv2.imshow("Camera",frame)
    cv2.setMouseCallback("Camera", on_mouse, frame)
    # 1 ms 동안 대기하며 키 입력을 받고 'q' 입력 시 종료
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
