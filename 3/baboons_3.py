from __future__ import print_function
from threading import Semaphore, Lock, Thread
from collections import deque
from random import random, randint
from time import sleep
import sys
import logging

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
    while True:
        with turnstile:
            switches[side].lock(rope)
        with multiplex:
            with mutex:
                crossing_side = side
                crossing.add(my_id)
                waiting[side].remove(my_id)
            sleep(random())  # crossing
            with mutex:
                crossing.remove(my_id)
                waiting[1 - side].add(my_id)
        switches[side].unlock(rope)
        side = 1 - side


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
        

ROPE_MAX    = 5
NUM_BABOONS = 10
side_names  = ['west', 'east']

if __name__ == '__main__':
    rope       = Lock()
    turnstile  = Lock()
    switches   = [Lightswitch(), Lightswitch()]
    multiplex  = Semaphore(ROPE_MAX)

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

    Thread(target=report).start()
