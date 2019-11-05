'''
The Charlie (source) node for the qBeggar project
'''

import sys
from cqc.pythonLib import CQCConnection, qubit

with CQCConnection("Charlie") as Charlie:
    for i in range(100):
        # Create two qubits
        qalice = qubit(Charlie)
        qbob = qubit(Charlie)

        # Use hadamard and cnot to create Bell state. I assume that qalice and qbob are changed
        qalice.H()
        qalice.cnot(qbob)

        # send the qubits
        Charlie.sendQubit("Alice", qalice)
        Charlie.sendQubit("Bob", qbob)

