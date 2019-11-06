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

correct_basis = []
correct_keyA = []
correct_keyB = []
#bits_alice = []    (apparently) useless (from BB84.py)
received_alice = []
#bits_bob = []      (apparently) useless (from BB84.py)
basis_bob = []
received_bob = []
modes_alice = []

angA_1 = 224
angA_2 = 32

clenght = 100




def preparation_Alice():
    with CQCConnection("Alice") as Alice:
        for i in range(clenght):
            q = Alice.recvQubit()
            sleep(0.01)
            rnd_mode_choice = int.from_bytes(Alice.recvClassical(), 'big')
            modes_alice.append(rnd_mode_choice)
            if rnd_mode_choice == 1:
                #print ("Key generation mode selected")
                #complete with key mode actions

                #q = Alice.recvQubit()
                basis_alice.append(0)               #key test on basis Z
                a = q.measure()
                if a == 0:
                    received_alice.append(+1)
                elif a == 1:
                    received_alice.append(-1)
                else:
                    print ("Error: measure != {0,1}")

            if rnd_mode_choice == 0:
                #print ("Control mode selected")
                #complete with control mode actions

                #q = Alice.recvQubit()                  #input is an (entangeld))qubit
                random_basis_alice = randint(0,1)
                basis_alice.append(random_basis_alice)

                if random_basis_alice == 0:           #basis 0 w/ angA_1
                    q.rot_Y(angA_1)
                    m = q.measure()
                    if m == 0:
                        received_alice.append(+1)
                    elif m == 1:
                        received_alice.append(-1)
                    else:
                        print ("Error: measure != {0,1}")

                if random_basis_alice == 1:           #basis 1 w/ angA_2
                    q.rot_Y(angA_2)
                    n = q.measure()
                    if n == 0:
                        received_alice.append(+1)
                    elif n == 1:
                        received_alice.append(-1)
                    else:
                        print ("Error: measure != {0,1}")
        for i in range(clenght):
            if modes_alice[i] == 0:
                sleep(0.01)
                Alice.sendClassical("Bob", basis_alice[i])
                sleep(0.01)
                Alice.sendClassical("Bob", received_alice[i]+1) 
        print ("modes of Alice ", modes_alice)           

preparation_Alice()
