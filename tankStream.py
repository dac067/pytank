#imports
import RPi.GPIO as GPIO
import curses
import cv2
import picamera
import picamera.array
import time

GPIO.setmode(GPIO.BOARD)

#Pin definitions
rightFwd = 7
rightRev = 11
leftFwd = 13
leftRev = 15
tiltServo = 12

#Pin setup and initialization
GPIO.setup(leftFwd, GPIO.OUT)
GPIO.setup(leftRev, GPIO.OUT)
GPIO.setup(rightFwd, GPIO.OUT)
GPIO.setup(rightRev, GPIO.OUT)
GPIO.setup(tiltServo,GPIO.OUT)

#PWM setupt
tilt = GPIO.PWM(tiltServo, 50)
rightMotorFwd = GPIO.PWM(rightFwd, 50)
leftMotorFwd = GPIO.PWM(leftFwd, 50)
rightMotorRev = GPIO.PWM(rightRev, 50)
leftMotorRev = GPIO.PWM(leftRev, 50)

#Keyboard setup
screen = curses.initscr()
curses.cbreak() #continuous readings
screen.keypad(1) #enable keypad
screen.nodelay(1) #no delay, getch returns -1 if no key pressed
keyPressed = True #key counter
key = ''
movementHold = False #counter so that movement functions only run once when key is held

#Disable movement at startup
GPIO.output(leftFwd, False)
GPIO.output(leftRev, False)
GPIO.output(rightFwd, False)
GPIO.output(rightRev, False)

def forward():
        rightMotorFwd.ChangeDutyCycle(45)
        leftMotorFwd.ChangeDutyCycle(45)
        print "Forward start"

def left():
        #leftMotorFwd.ChangeDutyCycle(45)
        rightMotorFwd.ChangeDutyCycle(30)
        print "Left"

def right():
        #rightMotorFwd.ChangeDutyCycle(45)
        leftMotorFwd.ChangeDutyCycle(30)
        print "Right"

def reverse():
        rightMotorRev.ChangeDutyCycle(45)
        leftMotorRev.ChangeDutyCycle(45)
        print "Reverse start"

def stop():
        GPIO.output(rightFwd, False)
        GPIO.output(leftFwd, False)
        GPIO.output(rightFwd, False)
        GPIO.output(leftFwd, False)
        rightMotorFwd.ChangeDutyCycle(0)
        rightMotorRev.ChangeDutyCycle(0)
        leftMotorFwd.ChangeDutyCycle(0)
        leftMotorRev.ChangeDutyCycle(0)
        tilt.ChangeDutyCycle(0)

def tiltUp():
        print "Tilt Up"
        tilt.ChangeDutyCycle(1)
        time.sleep(1)


def tiltFwd():
        print "Tilt Forward"
        tilt.ChangeDutyCycle(5)
        time.sleep(1)


def tiltDown():
        print "Tilt Down"
        tilt.ChangeDutyCycle(8)
        time.sleep(1)


def movement(keyTapped, moveFunct):
        #Create a delay when a key is initalled pressed to fix keyholding issue
        #e.g when a key is pressed and held, it doesnt register until moments later
        #so we need a delay after the initial press
        if keyTapped == True:
                curses.napms(500)
                moveFunct()
                keyTapped = False
        return keyTapped

tilt.start(0)
rightMotorFwd.start(0)
leftMotorFwd.start(0)
rightMotorRev.start(0)
leftMotorRev.start(0)

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)
	while key != ord('q'): # press q to quit
	        #Use cascading if/else statements so only one key registers at a time

		camera.capture(stream, format='bgr')
        	image = stream.array
		print image
            	cv2.imshow('frame', image)
	        key = screen.getch()
	        if key == curses.KEY_UP:
	                keyPressed = movement(keyPressed, forward)

	        elif key == curses.KEY_LEFT:
	                keyPressed = movement(keyPressed, left)

	        elif key == curses.KEY_RIGHT:
	                keyPressed = movement(keyPressed, right)

	        elif key == curses.KEY_DOWN:
	                keyPressed = movement(keyPressed, reverse)

	        elif key == ord('a'):
	                keyPressed = movement(keyPressed, tiltUp)

	        elif key == ord('s'):
	                keyPressed = movement(keyPressed, tiltFwd)

	        elif key == ord('d'):
	                keyPressed = movement(keyPressed, tiltDown)


	        else:
	                if keyPressed == False:
	                        print "Stopped"
	                        keyPressed = True
	                        stop()


	        screen.refresh()
	        curses.napms(40)
		stream.seek(0)
		stream.truncate()
			
cv2.destroyAllWindows()
curses.endwin()
stop()
tilt.stop()
rightMotorFwd.stop()
leftMotorFwd.stop()
rightMotorRev.stop()
leftMotorRev.stop()


GPIO.cleanup()

