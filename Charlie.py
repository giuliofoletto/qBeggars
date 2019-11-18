'''
The Charlie (source) node for the qBeggar project
'''

clenght = 256

import sys
from cqc.pythonLib import CQCConnection, qubit
from time import sleep

with CQCConnection("Charlie") as Charlie:
    for i in range(clenght):
        #print(i)
        # Create two qubits
        qalice = qubit(Charlie)
        qbob = qubit(Charlie)

        # Use hadamard and cnot to create Bell state. I assume that qalice and qbob are changed
        qalice.H()
        qalice.cnot(qbob)

        # send the qubits
        Charlie.sendQubit(qalice,"Alice")
        Charlie.sendQubit( qbob,"Bob")
        sleep(0.03)
