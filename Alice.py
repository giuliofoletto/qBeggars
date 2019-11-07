import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit
from time import sleep
from tkinter import *
import json
import numpy as np



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
KGM_measures_alice = []
KGM_measures_alice_official = []

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
            else:
                KGM_measures_alice.append(received_alice[i]+1)
        index = np.random.choice(len(KGM_measures_alice),10,replace=False)
        indexlist = list(index)
        print(indexlist)
        i=0
        while i < len(KGM_measures_alice):
            if i in indexlist:
                KGM_measures_alice_official.append(KGM_measures_alice[i])
            i += 1

        print("KGM Measures Sent: ", KGM_measures_alice_official)
        Alice.sendClassical("Bob", KGM_measures_alice_official)

        #Alice.sendClassical("Bob", index)
        #print ("modes of Alice ", modes_alice)

preparation_Alice()

#INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE

alice = Tk()

alice.title( "QBeggars - Alice" )

message = StringVar()
message.set(" ")
sent = StringVar()
sent.set(" ")

send_label = Label( alice, text = "Insert a message you want to send securely" )
send_label.pack()

entry = Entry(alice, bd = 5, textvariable = message)
entry.pack(fill=X)

#establish QKD and update Bob label
def QBeggars(s):
    print("ciò che arriva dalla casella", s)
    sent_bin_j = ' '.join(format(ord(x), 'b') for x in s)

    print("Stringa da inviare in binario: ", sent_bin_j)

    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob", sent_bin_j)
        print("Alice SENT: ", sent_bin_j)

#update labels and calls QBeggars when 'SEND!' is pressed
def callback():
    message_read = message.get()
    #sent_bin = ''.join( format(ord(i), 'b') for i in message.get() )
    sent_label.config( text = message_read )
    #sent_bin_label.config( text = sent_bin )
    entry.delete( first = 0, last = 100 )
    QBeggars(message_read)


sent_label = Label( alice, text = "Alice didn't send anything" )
sent_label.pack()
sent_bin_label = Label( alice, text = "Alice didn't send anything but in binary" )
sent_bin_label.pack()
send_button = Button( alice, text="SEND!", width=10, command=callback )
send_button.pack()


alice.mainloop()
