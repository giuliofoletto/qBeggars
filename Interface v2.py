from tkinter import *
import Charlie

alice = Tk()
bob = Tk()


alice.title( "QBeggars - Alice" )
bob.title( "QBeggars - Bob" )


#ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE-ALICE

message = StringVar()
message.set(" ")
sent = StringVar()
sent.set(" ")

send_label = Label( alice, text = "Insert a message you want to send securely" )
send_label.pack()

entry = Entry(alice, bd = 5, textvariable = message)
entry.pack(fill=X)

#establish QKD and update Bob label
def QBeggars():
    aggiunta = "Arrivato"
    received = message.get() + aggiunta
    receive_label.config( text = received )

#update labels and calls QBeggars when 'SEND!' is pressed
def callback():
    QBeggars()
    sent_bin = ''.join( format(ord(i), 'b') for i in message.get() )
    sent_label.config( text = message.get() )
    sent_bin_label.config( text = sent_bin )
    entry.delete( first = 0, last = 100 )


sent_label = Label( alice, text = "Alice didn't send anything" )
sent_label.pack()
sent_bin_label = Label( alice, text = "Alice didn't send anything but in binary" )
sent_bin_label.pack()
send_button = Button( alice, text="SEND!", width=10, command=callback )
send_button.pack()

#BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB-BOB

receive_label = Label( bob, text = "Bob didn't receive anything" )
receive_label.pack()

bob.mainloop()
