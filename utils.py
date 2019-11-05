'''
Some python utilities for the qBeggars project
'''

import numpy as np

# Compute the CHSH correlation value based on four binary arrays (bases are 0,1 whereas outcomes are +1,-1)
def compute_CHSH(alice_bases, alice_outcomes, bob_bases, bob_outcomes):
    outcomes = alice_outcomes*bob_outcomes
    a0b0 = np.mean(outcomes[np.logical_and(alice_bases == 0, bob_bases == 0)])
    a0b1 = np.mean(outcomes[np.logical_and(alice_bases == 0, bob_bases == 1)])
    a1b0 = np.mean(outcomes[np.logical_and(alice_bases == 1, bob_bases == 0)])
    a1b1 = np.mean(outcomes[np.logical_and(alice_bases == 1, bob_bases == 1)])
    s = a0b0 + a0b1 + a1b0 - a1b1
    return s

# Compute the binary entropy
def h2(x):
    return -1*x*np.log2(x)-(1-x)*np.log2(1-x)

# Compute the holevo quantity (see 10.1103/PhysRevLett.98.230501)
def holevo(s):
    arg = 0.5*(1+np.sqrt((s/2)**2-1))
    return h2(arg)

# find the positions in which arrayA differs from arrayB
def error_finder(arrayA, arrayB, maskA = None, maskB = None):
    if maskA == None:
        maskA = np.ones(arrayA.size, dtype = bool)
    if maskB == None:
        maskB = np.ones(arrayB.size, dtype = bool)
    if arrayA[maskA].size != arrayB[maskB].size:
        raise ValueError("Array sizes do not match")
    errors = (arrayA[maskB] != arrayB[maskB])
    return errors