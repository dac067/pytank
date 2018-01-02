from pynput import keyboard

def on_key_release(key):
	print('Released key %s' %key)

with keyboard.Listener(on_release = on_key_release) as listener:
	listener.join()
