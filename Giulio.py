# creare le coppie entangled dentro charlie e mando una a A e una B e lo faccio in un ciclo per 100 volte 
# esempio su EPR TELEPORTATION

import sys
from cqc.pythonLib import CQCConnection, qubit

# ho provato a farlo "da solo" ma ho seri dubbi che quello che ho scritto abbia alcun senso
  with CQCConnection("Charlie") as Charlie:
    for i in range(100):
        # creo due qbits
        qalice = qubit(Charlie)
        qbob = qubit(Charlie)

        apply_H(qalice) # mi pare di aver capito che per usare cnot dopo devo prima applicare Hadamard a uno dei due qbits ma non ho capito ne perche' ne cosa fa

        # applico cnot ai qbits
        apply_CNOT(qalice,qbob) # su wikipedia c'e' scritto che cnot ha bisogno di tre qbits e qui ne prende solo due, per cui non so bene a cosa serva questo

        # mando i qbits
        sendQubit(qalice,Alice)
        sendQubit(qbob,Bob)

# vi copio qua sotto il codice da teleportation

from cqc.pythonLib import CQCConnection, qubit

def send_teleportation(q,sender,receiver):
    qA = sender.createEPR(receiver)
    q.cnot(qA)
    q.H()
    a = q.measure()
    b = qA.measure()
    sender.sendClassical(receiver, [a, b])
    print('Corrections were sent at', sender, ':', [a, b])
    return [a,b]

def accept_teleportation(receiver):
    qB = receiver.recvEPR()
    message = list(receiver.recvClassical())
    print("data: ", message)
    if message[1] == 1:
        qB.X()
    if message[0] == 1:
        qB.Z()                         
    return qB