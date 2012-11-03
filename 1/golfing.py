# Ricco Amezcua, 11/3/12
# Created for CS450
# This program simulates golfers hitting balls down a drive concurrently and a cart
# picking up balls when a universal stash of balls has gotten too low.  This program
# is a test of using semaphores.

from threading import Semaphore, Thread, Lock
from random import random
from time import sleep
import sys

def cart():
	global stash, balls_on_field
	while True:
		insufficient_stash.acquire()
		print "#" * 70
		print "Stash = %d; The cart has entered the field" % stash
		stash += balls_on_field
		print "The cart has finished; the cart gathered %d balls; Stash = %d" % (balls_on_field, stash)
		print "#" * 70
		balls_on_field = 0
		full_stash.release()	

def golfer(my_id):
	global stash, balls_on_field
	bucket = 0
	sleep(random())
	while True:
		if bucket == 0:
			with mutex:
				print "Golfer %d calling for a bucket" % my_id
				if stash < BUCKET_SIZE:
					insufficient_stash.release()
					full_stash.acquire()
				stash -= BUCKET_SIZE
				bucket = BUCKET_SIZE
				print "Golfer %d got %d balls; Stash = %d" % (my_id, BUCKET_SIZE, stash)

		for i in range(bucket):
			sleep(random())
			print "Golfer %d hit ball %d" % (my_id, i)	
			bucket -= 1
			balls_on_field += 1
		

STASH_SIZE 	= int(raw_input("Size of stash?"))
BUCKET_SIZE = int(raw_input("Size of bucket?"))
NUM_GOLFERS = int(raw_input("Number of golfers?"))

if __name__ == '__main__':
	stash 										= STASH_SIZE
	balls_on_field 						= 0
	mutex 										= Semaphore(1)
	insufficient_stash 				= Semaphore(0)
	full_stash 								= Semaphore(0)

	gthreads = []
	for i in range(NUM_GOLFERS):
		tid = i
		gthreads.append(Thread(target=golfer, args=[tid]))

	c = Thread(target=cart)
	c.start()

	for t in gthreads:
		t.start()
	
