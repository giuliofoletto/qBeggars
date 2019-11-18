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
indexlist = []
angA_1 = 224
angA_2 = 32

clenght = 256


def preparation_Alice():
    global KGM_measures_alice, indexlist
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
        index = np.random.choice(len(KGM_measures_alice),int(0.1*len(KGM_measures_alice)),replace=False)
        indexlist = list(index)
        print(indexlist)
        i=0
        while i < len(KGM_measures_alice):
            if i in indexlist:
                KGM_measures_alice_official.append(KGM_measures_alice[i])
            i += 1

        print("KGM Measures Sent: ", KGM_measures_alice_official)
        sleep(0.01)
        Alice.sendClassical("Bob", KGM_measures_alice_official)
        sleep(0.01)
        Alice.sendClassical("Bob", indexlist)
        #print ("modes of Alice ", modes_alice)

def keyReconciliation(sift_key):
    sleep(0.01)
    correct_key_size = int.from_bytes(Alice.recvClassical(),'big')
    print('Alice corrected key size:', correct_key_size)
    correct_key = sift_key[0:correct_key_size]
    return correct_key

def privacyAmplification(cor_key):
    sleep(0.01)
    secret_key_size =  int.from_bytes(Alice.recvClassical(),'big')
    secret_key = cor_key[0:secret_key_size]
    return secret_key

preparation_Alice()
with CQCConnection("Alice") as Alice:

    sleep(0.01)
    success = int.from_bytes(Alice.recvClassical(),'big')
    if success:
        KGM_measures_alice =  np.array(KGM_measures_alice,dtype=int)
        mask = np.ones(KGM_measures_alice.size,dtype=bool)
        mask[indexlist]= 0
        sifted_key = KGM_measures_alice[mask]//2
        print('Sifted key Alice: ', sifted_key)
        correct_key = keyReconciliation(sifted_key)
        secret_key= privacyAmplification(correct_key)
        print('The following secret key of ', secret_key.size, 'bits was produced:' )
        print(secret_key)
    else: 
        print('Communication aborted')
        exit()


#INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE

alice = Tk()

alice.title( "QBeggars - Alice" )

message = StringVar()
message.set("")
sent = StringVar()
sent.set("")

send_label = Label( alice, text = "Insert a message you want to send securely" )
send_label.pack()

entry = Entry(alice, bd = 5, textvariable = message)
entry.pack(fill=X)

#establish QKD and update Bob label
def QBeggars(s):
    print("Prompted text to send: ", s)
    to_send_bin_j = ''.join(format(ord(x), 'b') for x in s)
    print("Text converted in binary: ", ' '.join(format(ord(x), 'b') for x in s))
    if secret_key.size < len(to_send_bin_j):
        print('The message is too long to apply OTP with the available key')
        return
    else:
        print("Binary key for OTP: ", secret_key[0:len(to_send_bin_j)])
        plaintext_bool = np.array(np.array(list(to_send_bin_j),int),bool)
        #print(plaintext_bool)
        key_bool = np.array(np.array(list(secret_key[0:len(to_send_bin_j)]),int),bool)
        #print(key_bool)
        cyphertext =  np.logical_xor(plaintext_bool, key_bool)
        #print(cyphertext)
        cyphertext = list(np.array(cyphertext,int))
        print("Binary cyphertext: ", cyphertext)
        char_idx = range(len(to_send_bin_j)//7)
        sent_bin_j = cyphertext
        #sent_bin_j = ' '.join(format(ord(cyphertext[7*idx:7*idx+7]), 'b') for idx in char_idx)
        #print(sent_bin_j)

    
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
