import sys
import tty
import termios

########################################################################

class RawInputWrapper(object):

  def __init__(self):
    fd = sys.stdin.fileno()
    self.old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)

  def cleanup(self):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSANOW, self.old_settings)

########################################################################
  
def getch():
  ch = sys.stdin.read(1)
  return ch

########################################################################
