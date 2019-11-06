import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit
from time import sleep



bits_alice = []
basis_alice = []
test = []
mesaj = []



def preperation_Alice():
    with CQCConnection("Alice") as Alice:
        for i in range(100):
            #q = Alice.recvQubit()
            sleep(0.01)
            rnd_mode_choice = Alice.recvClassical()
            if rnd_mode_choice == 1:
                print ("Key generation mode selected")
                #complete with key mode actions
            if rnd_mode_choice == 0:
                print ("Control mode selected")
                #complete with control mode actions

preperation_Alice()
