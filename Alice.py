import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import pool
from cqc.pythonLib import CQCConnection, qubit
from time import sleep
from tkinter import *
import json


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
    sent_bin_j = json.dumps(s).encode('utf-8')

    with CQCConnection("Alice") as Alice:
        Alice.sendClassical("Bob", sent_bin_j)
        print("Alice SENT: ", sent_bin_j)

#update labels and calls QBeggars when 'SEND!' is pressed
def callback():
    #sent_bin = ''.join( format(ord(i), 'b') for i in message.get() )
    sent_label.config( text = message.get() )
    #sent_bin_label.config( text = sent_bin )
    entry.delete( first = 0, last = 100 )
    QBeggars(message.get())


sent_label = Label( alice, text = "Alice didn't send anything" )
sent_label.pack()
sent_bin_label = Label( alice, text = "Alice didn't send anything but in binary" )
sent_bin_label.pack()
send_button = Button( alice, text="SEND!", width=10, command=callback )
send_button.pack()


alice.mainloop()
