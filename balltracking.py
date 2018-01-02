from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np
import imutils

defaultSpeed = 25
windowCenter = 320
centerBuffer = 30
pwmBound = float(25)
cameraBound = float(320)
kp = pwmBound / cameraBound
leftBound = int(windowCenter - centerBuffer)
rightBound = int(windowCenter + centerBuffer)
error = 0
ballPixel = 0

#GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Pin definitions
rightFwd = 7
rightRev = 11
leftFwd = 13
leftRev = 15

#GPIO initialization
GPIO.setup(leftFwd, GPIO.OUT)
GPIO.setup(leftRev, GPIO.OUT)
GPIO.setup(rightFwd, GPIO.OUT)
GPIO.setup(rightRev, GPIO.OUT)

#Disable movement at startup
GPIO.output(leftFwd, False)
GPIO.output(leftRev, False)
GPIO.output(rightFwd, False)
GPIO.output(rightRev, False)

#PWM Initialization

rightMotorFwd = GPIO.PWM(rightFwd, 50)
leftMotorFwd = GPIO.PWM(leftFwd, 50)
rightMotorRev = GPIO.PWM(rightRev, 50)
leftMotorRev = GPIO.PWM(leftRev, 50)
rightMotorFwd.start(defaultSpeed)
leftMotorFwd.start(defaultSpeed)
leftMotorRev.start(defaultSpeed)
rightMotorRev.start(defaultSpeed)
def pwmStop():
	rightMotorFwd.ChangeDutyCycle(0)
	rightMotorRev.ChangeDutyCycle(0)
	leftMotorFwd.ChangeDutyCycle(0)
	leftMotorRev.ChangeDutyCycle(0)

#Camera setup
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size = (640, 480))

time.sleep(0.1)

lower_yellow = np.array([15, 70, 70])
upper_yellow = np.array([40, 255, 255])

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	image = frame.array
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	ballPixel = 0
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x,y,), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
	
		
		if radius > 10:
			cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(image, center, 5, (0, 0, 255), -1)
			ballPixel = x
		else:
			ballPixel = 0
	
	#cv2.imshow("image", None)
	cv2.namedWindow("window")
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
		
	#Proportional controller
	if ballPixel == 0:
		print "no ball"
		error = 0
		pwmStop()
	elif (ballPixel < leftBound) or (ballPixel > rightBound):
		error = windowCenter - ballPixel
		pwmOut = abs(error * kp) 
		print radius
		if  ballPixel < (leftBound) and pwmOut > 7 and radius < 40:
			print "left side"
			rightMotorFwd.ChangeDutyCycle(pwmOut + defaultSpeed)
			leftMotorFwd.ChangeDutyCycle(defaultSpeed)
			#leftMotorRev.ChangeDutyCycle(pwmOut)
			#rightMotorRev.ChangeDutyCycle(0)
		elif ballPixel > (rightBound) and pwmOut > 7:
			print "right side"
			leftMotorFwd.ChangeDutyCycle(pwmOut + defaultSpeed)
			#rightMotorRev.ChangeDutyCycle(pwmOut)
			#leftMotorRev.ChangeDutyCycle(0)
			rightMotorFwd.ChangeDutyCycle(defaultSpeed)
	else:	
		print "middle"
		if (radius < 40):
			rightMotorFwd.ChangeDutyCycle(defaultSpeed)	
			leftMotorFwd.ChangeDutyCycle(defaultSpeed)
		else:
			pwmStop()
	if key == ord('q'):
		break

cv2.destroyAllWindows()
camera.close()
pwmStop()
GPIO.cleanup()


