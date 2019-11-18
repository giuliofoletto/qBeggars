import sys
from math import floor, ceil, log, sqrt, copysign
from random import randint, random, sample
from multiprocessing import Pool
from cqc.pythonLib import CQCConnection, qubit
from time import sleep
import utils
import numpy as np
from tkinter import *
import json
import struct


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
KGM_mesures_alice =[]
KGM_mesures_bob =[]
index = []

angB_1 = 0
angB_2 = 64

clenght = 256

def preparation_Bob():
    with CQCConnection("Bob") as Bob:
        p_control_mode = 0.5
        p_key_mode = 1-p_control_mode
        for i in range(clenght):
            print(i)
            q = Bob.recvQubit()
            sleep(0.01)
            rnd_mode_choice = int((random() > p_control_mode)) #we need positive values (0 or 1) to send them
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
        global KGM_mesures_bob
        for i in range(clenght):
            if modes_bob[i] == 0:
                sleep(0.01)
                Abasis = int.from_bytes(Bob.recvClassical(),"big")
                basis_alice.append(Abasis)
                sleep(0.01)
                Ameasure = int.from_bytes(Bob.recvClassical(),"big")-1
                received_alice.append(Ameasure)
            else:
                KGM_mesures_bob.append(received_bob[i]+1)
        print('Bob receiving now')
        global KGM_mesures_alice
        KGM_mesures_alice = list(bytearray(Bob.recvClassical()))
        KGM_mesures_alice_official = list(KGM_mesures_alice)        #questa è una lista con le misure che ha fatto alice, alla posizione indicata dall'indice.
        global index
        index = Bob.recvClassical()
        indexlist = list(index)                     #indexlist è una lista con gli indici scelti da alice
        print ("KGM Measures Received: ", KGM_mesures_alice_official)
        print ("index bob: ", indexlist)





        #for i in range(len(KGM_mesures_alice)):
        #    KGM_mesures_alice[i] = int.from_bytes(KGM_mesures_alice[i], "big")
        #index = Bob.recvClassical()
        #for i in range(len(index)):
        #    index[i] = int.from_bytes(index[i], "big")
        #KGM_mesures_bob = KGM_mesures_bob[index]

        #A_array = np.asarray(KGM_mesures_alice)
        #B_array = np.asarray(KGM_mesures_bob)
        #utils.error_finder(A_array,B_array)




    print ("basis of Bob ", basis_bob)
    print ("measures of Bob ", received_bob)
    print ("modes of Bob ", modes_bob)
    print ("basis of Alice ", basis_alice)
    print ("measures of Alice ", received_alice)



def calculate_QBER():
    error = 0
    for i in range(len(list(index))):
        if (KGM_mesures_alice[i] != KGM_mesures_bob[indexlist[i]]):
            error = error + 1
    print ("Key Sample Alice:", KGM_mesures_alice)
    print ("Key Sample Bob:", KGM_mesures_bob[indexlist])
    print ("error: ", error)
    error_percentage = error/len(indexlist) # maximum value is 1
    print("error_percentage: ", error_percentage)
    global qber
    # global qber2
    qber = error_percentage # lies btween 0 and 1
    print("qber:", qber)
    return qber


def secureKeyRate(s,qber):
    mutual_info_AB = 1 - utils.h2(qber)
    Eve_Holevo_bound = utils.holevo(s)
    secure_key_rate = max(mutual_info_AB - Eve_Holevo_bound, 0) #infinite key length approximation
    print('Secure key rate: ', secure_key_rate)
    return secure_key_rate

def keyReconciliation(sift_key,qber): #to be implemented seriously (eg. through Cascade alg. or LDPC code)
    mutual_info_rate = 1 - utils.h2(qber)
    correct_key_size = floor(sift_key.size * mutual_info_rate)
    print('Bob corrected key size:', correct_key_size)
    corrected_key = sift_key[0:correct_key_size]
    return corrected_key

def privacyAmplification(sift_key,corr_key,s): #to be implemented seriously through epsilon-universal hash functions (eg. Toeplitz matrices)
    Eve_info_rate = utils.holevo(s)
    print(Eve_info_rate)
    secret_key_length = corr_key.size - ceil(sift_key.size * Eve_info_rate)
    secret_key = corr_key[0:secret_key_length-1]
    return secret_key


preparation_Bob()
basis_alice = np.array(basis_alice,dtype=int)
received_alice = np.array(received_alice,dtype=int)
basis_bob = np.array(basis_bob,dtype=int)
received_bob = np.array(received_bob,dtype=int)
modes_bob = np.array(modes_bob,dtype=int)   
S=utils.compute_CHSH(basis_alice, received_alice, basis_bob[modes_bob == 0], received_bob[modes_bob == 0])
print(S)
KGM_mesures_bob = np.array(KGM_mesures_bob,dtype=int)
indexlist = sorted(list(index))
QBER = calculate_QBER()
secret_key_rate= secureKeyRate(S,QBER)
with CQCConnection("Bob") as Bob:
    if secret_key_rate == 0:
        print('The transmission is too disturbed to establish a secret key.')
        Bob.sendClassical("Alice",0) 
    else:
        Bob.sendClassical("Alice",1)
        sleep(0.01)
        mask = np.ones(KGM_mesures_bob.size,dtype=bool)
        mask[indexlist]= 0
        sifted_key = KGM_mesures_bob[mask]//2
        print('Sifted key Bob :', sifted_key)
        correct_key = keyReconciliation(sifted_key,QBER)
        Bob.sendClassical("Alice",correct_key.size)
        sleep(0.01)
        secret_key = privacyAmplification(sifted_key,correct_key,S)
        Bob.sendClassical("Alice",secret_key.size)
        print('The following secret key of ', secret_key.size, 'bits was produced:' )
        print(secret_key)
    

#INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE INTERFACE


with CQCConnection("Bob") as Bob:
    received_j = list(bytearray(Bob.recvClassical(msg_size=10000)))
    print("Received cyphertext: ", received_j)
    cyphertext_bool = np.array(np.array(received_j,int),bool)
    key_bool = np.array(np.array(list(secret_key[0:len(received_j)]),int),bool)
    #print(key_bool)
    plaintext_b =  np.logical_xor(cyphertext_bool, key_bool)
    #print(plaintext_b)
    plaintext_b = list(np.array(plaintext_b,int))
    print("Binary plaintext: ", plaintext_b)
    plaintext=[]
    for i in range((len(plaintext_b))//7):
        byte = plaintext_b[7*i:7*(i+1)]
        print(byte)
        num=0
        for j in range(7):
            num += byte[6-j]*(2**j)
        print(num,chr(num))
        plaintext.append(chr(num))
    plaintext = ''.join(plaintext)
    print('Decoded text', plaintext)
    


bob = Tk()
bob.title( "QBeggars - Bob" )
receive_label = Label( bob, text = "Cyphered communication from Alice: \n" + plaintext )
receive_label.pack()

bob.mainloop()
