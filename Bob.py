import sys
from math import ceil, log, sqrt, copysign
from random import randint, random, sample
from multiprocessing import Pool
from cqc.pythonLib import CQCConnection, qubit
from time import sleep
import utils
import numpy as np
from tkinter import *
import json


correct_basis = []
correct_keyA = []
correct_keyB = []
bits_alice = []
basis_alice = []
bits_bob = []
basis_bob = []
received_alice = []
received_bob = []
modes_bob = []

angB_1 = 0
angB_2 = 64

clenght = 100

def preparation_Bob():
    with CQCConnection("Bob") as Bob:
        p_control_mode = 0.5
        p_key_mode = 1-p_control_mode
        for i in range(clenght):
            print(i)
            q = Bob.recvQubit()
            sleep(0.01)
            rnd_mode_choice = int((copysign(1,(random()-p_control_mode))+1)/2) #copysign used to get +1 or -1 but never 0, then we need to turn those into positive values (0 or 1) to send them
            Bob.sendClassical("Alice", rnd_mode_choice)
            modes_bob.append(rnd_mode_choice)
            sleep(0.01)
            if rnd_mode_choice == 1:
                print ("Key generation mode selected")
                #complete with key mode actions

                #q = Bob.recvQubit()
                basis_bob.append(2)               #key test on basis Z (flag "2")
                a = q.measure()
                if a == 0:
                    received_bob.append(+1)
                elif a == 1:
                    received_bob.append(-1)
                else:
                    print ("Error: measure != {0,1}")

            if rnd_mode_choice == 0:
                print ("Control mode selected")
                #complete with control mode actions

                #q = Bob.recvQubit()
                random_basis_bob = randint(0,1)
                basis_bob.append(random_basis_bob)

                if random_basis_bob == 0:           #basis 0 w/ angB_1
                    q.rot_Y(angB_1)
                    m = q.measure()
                    if m == 0:
                        received_bob.append(+1)
                    elif m == 1:
                        received_bob.append(-1)
                    else:
                        print ("Error: measure != {0,1}")

                if random_basis_bob == 1:           #basis 1 w/ angB_2
                    q.rot_Y(angB_2)
                    n = q.measure()
                    if n == 0:
                        received_bob.append(+1)
                    elif n == 1:
                        received_bob.append(-1)
                    else:
                        print ("Error: measure != {0,1}")
        for i in range(clenght):
            if modes_bob[i] == 0:
                sleep(0.01)
                Abasis = int.from_bytes(Bob.recvClassical(),"big")
                basis_alice.append(Abasis)
                sleep(0.01)
                Ameasure = int.from_bytes(Bob.recvClassical(),"big")-1
                received_alice.append(Ameasure)


    print ("basis of Bob ", basis_bob)
    print ("measures of Bob ", received_bob)
    print ("modes of Bob ", modes_bob)
    print ("basis of Alice ", basis_alice)
    print ("measures of Alice ", received_alice)



def calculate():
    error = 0
    for i in range(len(received_alice)):
        if (basis_alice[i] == basis_bob[i]):
            correct_basis.append(i)
            correct_keyA.append(received_alice[i])
            correct_keyB.append(received_bob[i])
        else:
            error = error + 1
    print ("Correct Basis: ", correct_basis)
    print ("Correct Key Alice:", correct_keyA)
    print ("Correct Key Bob:", correct_keyB)
    print ("error: ", error)
    error_percentage = error/len(received_alice) # maximum value is 1
    print("error_percentage: ", error_percentage)
    size = ceil(sqrt(len(correct_basis)))
    print ("size: ", size)
    global qber
    global qber2
    qber = error_percentage/size # lies btween 0 and 1
    print("qber:", qber)

#def calculate():
 #   error = 0
  #  for i in range(len(received_bob)):
   #     if (basis_alice[i] == basis_bob[i]):
    #        correct_basis.append(i)
     #       correct_key.append(received[i])
      #  else:
  #          error = error + 1
  #  print ("Correct Basis: ", correct_basis)
  #  print ("Correct Key :", correct_key)
  #  print ("error:", error)
  #  error_percentage = error/len(received) # maximum value is 1
  #  print("error_percentage", error_percentage)
  #  size = ceil(sqrt(len(correct_basis)))
  #  print ("size: ", size)
  #  global qber
  #  global qber2
  #  qber = error_percentage/size # lies btween 0 and 1
  #  print("qber:", qber)

# def secureKeyRate(x):
  #  return ((-x)*log(x, 2) - (1-x)*log(1-x, 2))


preparation_Bob()
basis_alice = np.array(basis_alice,dtype=int)
received_alice = np.array(received_alice,dtype=int)
basis_bob = np.array(basis_bob,dtype=int)
received_bob = np.array(received_bob,dtype=int)
modes_bob = np.array(modes_bob,dtype=int)
S=utils.compute_CHSH(basis_alice, received_alice, basis_bob[modes_bob == 0], received_bob[modes_bob == 0])
print(S)


#INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE


with CQCConnection("Bob") as Bob:
    received_j = Bob.recvClassical(msg_size=10000)
    measure_outcome = json.loads(received_j.decode('utf-8'))
    print("FAK")
    type(measure_outcome)


bob = Tk()
bob.title( "QBeggars - Bob" )
receive_label = Label( bob, text = "Bob didn't receive anything" )
receive_label.pack()

bob.mainloop()
