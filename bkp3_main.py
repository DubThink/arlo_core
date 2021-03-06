#!/usr/bin/env python3
from pyvmu.vmu931 import VMU931Parser
from pyvmu.vmu931 import messages
from pyquaternion import Quaternion
import numpy as np
import time
from propellor import plink
import serial
import sys

print(sys.version)

vmuaddr2="/dev/serial/by-id/usb-Variense_VMU931_9312C34D80-if00"
vmuaddr="/dev/serial/by-id/usb-Variense_IMU_931D566612-if00"
hataddr="/dev/serial/by-id/usb-Parallax_Inc_Propeller_Activity_Brd_WX-if00-port0"

wait_time=0.1
def meter(v):
	s= "<--------------^-------------->"
	s=s[:15+int(v*14)]+"|"+s[16+int(v*14):]
	return s


# outer loop runs to start vmu and run the main loop
def run(pp):
	while True:
		try:
			print("Starting vmu...",end="")
			vp=VMU931Parser(device=vmuaddr,euler=False,quaternion=True)
			print("SUCCESS")
#			print("Timeout val:")
#			vp.ser.timeout=3
		except serial.serialutil.SerialException as e:
			print("FAIL")
			print(e)
			time.sleep(1)
		else:
			with vp:
				run_core(pp,vp)

# main loop - runs to keep propellor link open
def run_core(pp,vp):
	ltime=time.time()
	last_open_time=time.time()
	while True: # run loop
		try:
		#	print("run 1")
			packet=vp.parse()
		except serial.serialutil.SerialException as e:
			print("VMU read failed:",e)
			if not pp is None:
				pp.sendspeed(0,0)
			return
		else:
			if pp != None and pp.s.isOpen():
				# connected but not open
				# if this exists for too long, pring a message and close the connection
				if last_open_time+6000<time.time(): #timeout of 5 seconds
					print(" PROPELLOR SERIAL CONNECTED BUT NOT OPEN FOR TOO LONG, CLOSING...")
					pp_good=0
					pp.close()
					pp=None
			if pp != None and pp.s.isOpen() and ltime+wait_time<time.time():
				#print("open status:",pp.s.isOpen())
				try:
					refresh_cooldown= cycle(packet, vp)
					if(refresh_cooldown):
						ltime=time.time()
				except serial.serialutil.SerialException as e:
					print("&&&&&&&&&&",e)
					print("Propellor comms failed, attempting to restart... ")
					while 1:
						try:
							print("Reconnecting to propellor...",end="")
							pp.s.close()
							time.sleep(5)
							pp.s.open()
						except serial.serialutil.SerialException as e:
							print("FAILED")
						else:
							print("SUCCESS")
							break
'''if not pp is None:
					pp.s.close()
				try:
					pp=plink(hataddr)
				except serial.serialutil.SerialException as f:
					pp=None
					time.sleep(1)
				else:
					pp_good=True
					print("Propellor restarted")
					time.sleep(5)
					ltime=time.time()
					last_open_time=time.time()
'''			
def cycle(packet,vp):
			if type(packet) is messages.Quaternion:
				a=Quaternion(packet.w,packet.x,packet.y,packet.z)
				vec=[0,0,1]*np.matrix(a.rotation_matrix)
				x=np.arcsin(vec.T[0])/1.6
				y=np.arcsin(vec.T[1])/1.6
				z=np.arcsin(vec.T[2])/1.6
#				print(meter(x),"        ",meter(y),"    ",meter(z),y)
				if y>0:
#					print(int(z*9),int(x*11))
					pp.sendspeed(int(z*9),int(x*11))
				else:
					pp.sendspeed(0,0)
				return 1 # good packet
			else:
				return 0

if __name__=="__main__":
	while True:
		try:
			pp=plink(hataddr)
		except serial.serialutil.SerialException as e:
			time.sleep(1)
			print("No connection to propellor, retrying")
		else:
			print("Propellor connected")
			run(pp)
#			try:
#				run(pp)
#			except KeyboardInterrupt:
#				pp.sendspeed(0,0)
#				break

