# controller.py

# By Brendan Payne

# Description: 
# Uses inputs from a Dualshock 4 controller to intereact with a Neato botvac


DEVICE = '/dev/ttyACM0'

import serial
import time
import pygame

robot = serial.Serial(DEVICE) # connect to serial bus on Neato

U_D, L_R = 0,1 # X&Y on left analog stick

DIST = 10000 # set to an absurd amount 

SPEED = 200 # max 350

def docommand(port, command): 
	port.write((command + '\n').encode()) # sends encoded command to bot

docommand(robot, 'testmode on')

docommand(robot, 'playsound soundid 0')

def drive(self, x, y):
	#print("X:"+str(x)+" Y:"+str(y))
	if x==0 and y==0:
		docommand(self, "setmotor lwheeldist 1 rwheeldist 1 speed 1") # small values act as a brake
	if y==0:
		if x>0:
			lft,rgt = 1,0
		elif x<0:
			lft,rgt = 0,1
		else:
			lft,rgt = 0,0
	else:
		if x>0:
			lft,rgt = 1, 0.5
		elif x<0:
			lft,rgt = 0.5, 1
		else:
			lft,rgt = 1,1
		lft *= y
		rgt *= y
	docommand(self, "setmotor lwheeldist "+str(-lft*DIST)+" rwheeldist "+str(-rgt*DIST)+" speed "+str(SPEED))

if pygame:
	pygame.init()
	pygame.joystick.init()
	if pygame.joystick.get_count() > 0:
		controller = pygame.joystick.Joystick(0)
		controller.init()
		print(controller.get_name()+' Detecteted')
		while True: # continually checks for controller input
			time.sleep(0.2) # delay to prevent overload
			pygame.event.pump()
			drive(robot, controller.get_axis(U_D), controller.get_axis(L_R))
	else:
		print('No Joystick Found')
