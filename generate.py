#!/usr/bin/env python
import os
import pika
import psutil
import socket
import sys

from gpiozero import CPUTemperature
from time import sleep, time

def measure_temp():
	cpu = CPUTemperature()
	return cpu.temperature

def get_load():
	return os.getloadavg()
try:
	connection = pika.BlockingConnection( pika.ConnectionParameters(host='192.168.3.107'))
	channel = connection.channel()
	channel.queue_declare(queue='test')
except:
	print("Unexpected error:", sys.exc_info()[0])
	raise

current_milli_time = lambda: int(round(time() * 1000))
hostname = socket.gethostname()

while True:
	message = '{"hostname": "%s", "temp": %f, "time": %d, "load": [%f, %f, %f], "cpu_percentage": %f}' %(hostname, measure_temp(), current_milli_time(), *get_load(), psutil.cpu_percent())
	channel.basic_publish(exchange='', routing_key='test', body=message)
	print(" [x] Sent %r" % message)
	sleep(1)
connection.close()

