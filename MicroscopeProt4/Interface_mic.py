import serial
import time
from multiprocessing import Process
s=serial.Serial('/dev/ttyACM1',115200)

def x_s(pasos,dir,time_):
	s.write('x,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def y_s(pasos,dir,time_):
	s.write('y,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def z_s(pasos,dir,time_):
	s.write('z,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def brigthness(b):
	s.write('l,'+str(0)+','+str(0)+','+str(0)+','+str(b))
	time.sleep(0.01)
def auto(time_):
	y_s(2000,1,time_)
	time.sleep(3)
	for i in range(10):
		time.sleep(0.5)
		y_s(2000,0,time_)
		time.sleep(5)
		x_s(30,1,time_)
		time.sleep(0.5)
		y_s(2000,1,time_)
		time.sleep(5)
		x_s(30,1,time_)
def proc_H_y():
    while(1):
        s.write('y,'+str(20)+','+str(0)+','+str(500))
        time.sleep(0.01)
        #print 'home y'
def proc_H_x():
    while(1):
        s.write('x,'+str(20)+','+str(1)+','+str(500))
        time.sleep(0.01)
        #print 'home x'

H_y_ = Process(target=proc_H_y)
H_x_ = Process(target=proc_H_x)

def home():
	global H_y_
	global H_x_

	H_y_.start()
	print('aqui')
	if (s.readline()[0]=='y'):
		H_y_.terminate()
	H_y_ = Process(target=proc_H_y)
	time.sleep(0.05)
	H_x_.start()
	if (s.readline()[0]=='x'):
		time.sleep(0.05)
		H_x_.terminate()
	H_x_ = Process(target=proc_H_x)
	time.sleep(0.5)
	x_s(3000,0,500)
	time.sleep(1.5)
	y_s(300,1,500)