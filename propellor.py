import serial, time, struct
class plink:
	def __init__(self,addr):
		self.s= serial.Serial(addr)

	def rr(self):
		while self.s.in_waiting:
			print(self.s.read(self.s.in_waiting).strip().decode())

	def converse(self,a):
#		if self.s.isOpen():
			self.s.write(a)
#		time.sleep(.2)
			self.rr()
#		else:
#			print("plink: link not open")

	def sendspeed(self,x,y):
		self.converse(struct.pack("B",self.make_speed_byte(x,y)))

	def make_speed_byte(self,x,y):
		# x int in range -3, 4 (because less need of fast reverse)
		# y int in range -4,4
		x=int(x)
		y=int(y)
		if x>4:
			x=4
		if x<-3:
			x=-3
		if y<-4:
			y=-4
		if y>4:
			y=4
			#return 0x00 # 0 byte does nothing
		#adjust so positive
		x+=3
		y+=4
		#now each takes 3 bits
		return 0x80 | x<<4 | y

	def break_speed_byte(self,c):
		if (c&0x80)==128:
			x_desired=((c>>4)&0x7)-3;
			y_desired=(c&0xf)-4;
			return x_desired,y_desired

	def msb(self,x,y):
		return bin(make_speed_byte(x,y))
