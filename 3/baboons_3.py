from __future__ import print_function
from threading import Semaphore, Lock, Thread
from collections import deque
from random import random, randint
import random
from time import sleep
import sys
import logging
from timeit import Timer

class Lightswitch:
    def __init__(self):
        self.mutex = Lock()
        self.count = 0

    def lock(self, sem):
        with self.mutex:
            self.count += 1
            if self.count == 1:
                sem.acquire()

    def unlock(self, sem):
        with self.mutex:
            self.count -= 1
            if self.count == 0:
                sem.release()


def act_as_baboon(my_id, init_side):
    side = init_side
    random.seed(my_id)
    for i in xrange(NUM_CROSSINGS):
        with turnstile:
            switches[side].lock(rope)
        with multiplex:
            sleep(random.random())  # crossing; Seeded random number
        switches[side].unlock(rope)
        side = 1 - side
    print ("Baboon %d finished" % my_id)



# The sim function will run the actual simulation so that the main
# function can do the timing
def sim():
		# Declaring all the variables as global so they can be modified by the baboon func
    global turnstile
    global switches
    global rope
    global multiplex
    global mutex

    rope       = Lock()
    turnstile  = Lock()
    switches   = [Lightswitch(), Lightswitch()]
    multiplex  = Semaphore(ROPE_MAX)
    mutex      = Lock()

    #random.seed(100) # Used for choosing sides

    bthreads   = []
    for i in range(NUM_BABOONS):
        bid, bside = i, randint(0, 1)
        bthreads.append(Thread(target=act_as_baboon, args=[bid, bside]))

    for t in bthreads:
        t.start()
		
    for t in bthreads:
        t.join()
    
# These are the tunable variables for changing the simulation
ROPE_MAX    = 5
NUM_SIM     = 5
NUM_BABOONS = 10
NUM_CROSSINGS = 10
side_names  = ['west', 'east']

if __name__ == '__main__':
    sim_times = []
    print("Timing %d simulations with %d baboons, %d crossings:" % (NUM_SIM, NUM_BABOONS, NUM_CROSSINGS)) 
    print("-" * 50)
    for i in range(NUM_SIM):
        timer = Timer(sim)
        sim_times.append(timer.timeit(1))
        print("-" * 50)

    #print(sim_times)
    print("The total time elapsed: %0.4fs" % (sum(sim_times)))
    print("Avg. time per run: %0.4fs" % (sum(sim_times)/NUM_SIM)) 
