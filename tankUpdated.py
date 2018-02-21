#Imports
import RPi.GPIO as GPIO
import time
import curses
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
def forward():
	rightMotorFwd.ChangeDutyCycle(45)	
	leftMotorFwd.ChangeDutyCycle(45)	
	print 'Forward start \n'

def left():
	leftMotorRev.ChangeDutyCycle(30)
	rightMotorFwd.ChangeDutyCycle(60)
	print 'Left'

def right():
	rightMotorRev.ChangeDutyCycle(30)
	leftMotorFwd.ChangeDutyCycle(60)
	print 'Right \n'
	
def reverse():
	rightMotorRev.ChangeDutyCycle(47)
	leftMotorRev.ChangeDutyCycle(50)
	print 'Reverse start \n'
	
def stop():
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

while key != ord('q'): # press q to quit
	#Use cascading if/else statements so only one key registers at a time
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
			print 'Stopped \n'
			keyPressed = True
			stop()
		
	        
	screen.refresh()
	curses.napms(40)

curses.endwin()	
stop()
tilt.stop()
rightMotorFwd.stop()
leftMotorFwd.stop()
rightMotorRev.stop()
leftMotorRev.stop()	
	

GPIO.cleanup()
