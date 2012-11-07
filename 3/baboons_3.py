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
    global crossing_side
    side = init_side
    random.seed(my_id)
    for i in xrange(NUM_CROSSINGS):
        with turnstile:
            switches[side].lock(rope)
        with multiplex:
            with mutex:
                crossing_side = side
                crossing.add(my_id)
                waiting[side].remove(my_id)
            sleep(random.random())  # crossing; Seeded random number
            with mutex:
                crossing.remove(my_id)
                waiting[1 - side].add(my_id)
        switches[side].unlock(rope)
        side = 1 - side
    print ("Baboon %d finished" % my_id)

#def run_baboon(t):
    #t.run()
    #t.join()


# The sim function will run the actual simulation so that the main
# function can do the timing
def sim():
		# Declaring all the variables as global so they can be modified by the baboon func
    global turnstile
    global switches
    global rope
    global multiplex
    global mutex
    global waiting
    global crossing
    global crossing_side

    rope       = Lock()
    turnstile  = Lock()
    switches   = [Lightswitch(), Lightswitch()]
    multiplex  = Semaphore(ROPE_MAX)

    #random.seed(100) # Used for choosing sides

    # reporting structures
    mutex         = Lock()
    waiting       = [set(), set()]
    crossing      = set()
    crossing_side = None

    bthreads   = []
    for i in range(NUM_BABOONS):
        bid, bside = i, randint(0, 1)
        waiting[bside].add(bid)
        bthreads.append(Thread(target=act_as_baboon, args=[bid, bside]))

    for t in bthreads:
        t.start()
		
    for t in bthreads:
        t.join()
    
    #for t in bthreads:
        #tim = Timer(lambda:run_baboon(t))
        #print(tim.timeit(number=1))


# This reporting function is no longer used with the
# new timing
def report():
    while True:
        sleep(1)
        with mutex:
            if crossing_side is None:
                continue
            print(repr(waiting[0]).rjust(30), end=' ')
            if crossing_side == 0:
                print('---', end='')
            else:
                print('<--', end='')
            print(repr(crossing).center(17), end=' ')
            if crossing_side == 0:
                print('-->', end=' ')
            else:
                print('---', end=' ')
            print(waiting[1])


# These are the tunable variables for changing the simulation
ROPE_MAX    = 5
NUM_SIM     = 3
NUM_BABOONS = 5
NUM_CROSSINGS = 20
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
