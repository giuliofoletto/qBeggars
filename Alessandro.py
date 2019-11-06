import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import Pool
from cqc.pythonLib import CQCConnection, qubit

correct_basis = []
correct_keyA = []
correct_keyB = []
#bits_alice = []    (apparently) useless (from BB84.py)
basis_alice = []
received_alice = []
#bits_bob = []      (apparently) useless (from BB84.py)
basis_bob = [] 
received_bob = []

angA_1 = 0
angA_2 = 180
angB_1 = 90
angB_2 = 270


def preparation_Alice():
    with CQCConnection("Alice") as Alice:
        for i in range(100):
            
            q = Alice.recvEPR()                  #input is an EPR qubit
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


def preparation_Bob():
    with CQCConnection("Bob") as Bob:
        for i in range(100):
            
            q = Bob.recvEPR()
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
            
        # r = Bob.recvClassical()               not used (from BB84.py)
        # basis_alice[:] = list(r)
        
    # print ("basis of bob ", basis_bob)                     not used (from BB84.py)
    # print ("measurement results of bob: ",received)        not used (from BB84.py)
    # print ("received basis by bob ",basis_alice)           not used (from BB84.py)



def printresults():
    print ("basis of Alice ", basis_alice)
    print ("basis of Bob ", basis_bob)
    print ("measures of Alice ", received_alice)
    print ("measures of Bob ", received_bob)






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

def secureKeyRate(x):
    return ((-x)*log(x, 2) - (1-x)*log(1-x, 2))


if __name__ == "__main__":

    preparation_Alice()
    preparation_Bob()
    printresults()
    calculate()

