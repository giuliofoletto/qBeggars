import sys
from math import ceil, log, sqrt, copysign
from random import randint, random, sample
from multiprocessing import Pool
from cqc.pythonLib import CQCConnection, qubit
from time import sleep

correct_basis = []
correct_key = []
bits_alice = []
basis_alice = []
bits_bob = []
basis_bob = []
received = []

def preparation_Bob():
    with CQCConnection("Bob") as Bob:
        p_control_mode = 0.1
        p_key_mode = 1-p_control_mode
        for i in range(100):
            #q = Bob.recvQubit()
            rnd_mode_choice = int((copysign(1,(random()-p_control_mode))+1)/2) #copysign used to get +1 or -1 but never 0, then we need to turn those into positive values (0 or 1) to send them
            Bob.sendClassical("Alice", rnd_mode_choice)
            sleep(0.01)
            if rnd_mode_choice == 1:
                print ("Key generation mode selected")
                #complete with key mode actions
            if rnd_mode_choice == 0:
                print ("Control mode selected")
                #complete with control mode actions




def calculate():
    error = 0
    for i in range(len(received)):
        if (basis_alice[i] == basis_bob[i]):
            correct_basis.append(i)
            correct_key.append(received[i])
        else:
            error = error + 1
    print ("Correct Basis: ", correct_basis)
    print ("Correct Key :", correct_key)
    print ("error:", error)
    error_percentage = error/len(received) # maximum value is 1
    print("error_percentage", error_percentage)
    size = ceil(sqrt(len(correct_basis)))
    print ("size: ", size)
    global qber
    global qber2
    qber = error_percentage/size # lies btween 0 and 1
    print("qber:", qber)

def secureKeyRate(x):
    return ((-x)*log(x, 2) - (1-x)*log(1-x, 2))


preparation_Bob()
