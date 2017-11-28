#!/usr/bin/env python3
# Example using a character LCD plate.
import time

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

# create some custom characters
lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])

# Show some basic colors.
lcd.set_color(1.0, 0.0, 0.0)
lcd.clear()
lcd.message('START \x01')
time.sleep(1.0)

# Show button state.
lcd.clear()
lcd.message('Press buttons...')

# Make list of button value, text, and backlight color.
buttons = [ [LCD.SELECT, 'Select', (1,1,1),False],
            [LCD.LEFT,   'Left'  , (1,0,0),False],
            [LCD.UP,     'Up'    , (0,0,1),False],
            [LCD.DOWN,   'Down'  , (0,1,0),False],
            [LCD.RIGHT,  'Right' , (1,0,1),False] ]

print('Press Ctrl-C to quit.')

import main

select_down_time=0

while True:
	# Loop through each button and check if it is pressed.
	for button in buttons:
		if lcd.is_pressed(button[0]) and not button[3]:
			# Button is pressed, down
			if button[0] is LCD.SELECT:
				select_down_time=time.time()
				if not main.isLoopActive():
					# select button
					main.startLoop()
					lcd.clear()
					lcd.message("Starting")
				else:
					lcd.clear()
					if not main.toggleMovement():
						lcd.message("Disabled movement")
					else:
						lcd.message("Enabled movement")

		# log current key state (end of loop)
		button[3]= lcd.is_pressed(button[0])

	if lcd.is_pressed(LCD.SELECT) and buttons[0][3]  and time.time()-select_down_time>5:
		print("DEBUG down_time=",select_down_time)
		lcd.clear()
		lcd.message("Stopping...")
		main.stopLoop()
		lcd.set_cursor(0,1)
		lcd.message("Stopped")
#		save button state
