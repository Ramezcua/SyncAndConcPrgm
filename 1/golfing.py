from threading import Semaphore, Thread
from random import random
from time import sleep
import sys

def cart():
	while True:
		sleep(random() * 5 )
		print "I am a cart"

def golfer(my_id):
	while True:
		sleep(random() * 5)
		print "I am golfer %d" % my_id

STASH_SIZE 	= 20
BUCKET_SIZE = 5
NUM_GOLFERS = 5

if __name__ == '__main__':
	stash = STASH_SIZE

	gthreads = []
	for i in range(NUM_GOLFERS):
		tid = i
		gthreads.append(Thread(target=golfer, args=[tid]))

	c = Thread(target=cart)
	c.start()

	for t in gthreads:
		t.start()
	
