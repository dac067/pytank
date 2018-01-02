import curses
import time

screen = curses.initscr()
curses.cbreak()
screen.keypad(1)
screen.nodelay(1)
keyPressed = False
key = ''
i = 0

while key != ord('q'):  # press <Q> to exit the program
    key = screen.getch()  # get the key
    if key == ord('w'):
	if keyPressed == True:
		print "Forward"
		time.sleep(0.45)
		keyPressed = False
    else:
	if keyPressed == False:
		print "Stopped"
	keyPressed = True
    	
    screen.refresh()
    time.sleep(0.05)

    # the same, but for <Up> and <Down> keys:
    if key == curses.KEY_UP:
        screen.addstr(0, 0, "Up")
    elif key == curses.KEY_DOWN:
        screen.addstr(0, 0, "Down")

curses.endwin()
