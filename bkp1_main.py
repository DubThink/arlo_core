#!/usr/bin/env python3
from pyvmu.vmu931 import VMU931Parser
from pyvmu.vmu931 import messages
from pyquaternion import Quaternion
import numpy as np
import time
from propellor import plink

vmuaddr="/dev/serial/by-id/usb-Variense_VMU931_9312C34D80-if00"
hataddr="/dev/serial/by-id/usb-Parallax_Inc_Propeller_Activity_Brd_WX-if00-port0"
wait_time=0.1
def meter(v):
	s= "<--------------^-------------->"
	s=s[:15+int(v*14)]+"|"+s[16+int(v*14):]
	return s


def run(pp):
	with VMU931Parser(device=vmuaddr,euler=False,quaternion=True) as vp:
		ltime=time.time()
		while True:
			packet=vp.parse()
			if type(packet) is messages.Quaternion and time.time()-ltime>wait_time:
				ltime=time.time()
				a=Quaternion(packet.w,packet.x,packet.y,packet.z)
				vec=[0,0,1]*np.matrix(a.rotation_matrix)
				x=np.arcsin(vec.T[0])/1.6
				y=np.arcsin(vec.T[1])/1.6
				z=np.arcsin(vec.T[2])/1.6
#				print(meter(x),"        ",meter(y),"    ",meter(z),y)
				if y>0:
					print(int(z*7),int(x*7))
					pp.sendspeed(int(z*7),int(x*7))
				else:
					pp.sendspeed(0,0)
				

if __name__=="__main__":
	pp=plink(hataddr)
	try:
		run(pp)
	except KeyboardInterrupt:
		pp.sendspeed(0,0)

