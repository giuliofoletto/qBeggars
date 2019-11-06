from tkinter import *

main = Tk()

main.title( "QBeggars security communication" )

message = StringVar()
message.set(" ")
sent = StringVar()
sent.set(" ")

send_label = Label( main, text = "Insert a message you want to send securely" )
send_label.pack()

entry = Entry(main, bd = 5, textvariable = message)
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


sent_label = Label( main, text = "Alice didn't send anything" )
sent_label.pack()
sent_bin_label = Label( main, text = "Alice didn't send anything but in binary" )
sent_bin_label.pack()
receive_label = Label( main, text = "Bob didn't receive anything" )
receive_label.pack()
send_button = Button( main, text="SEND!", width=10, command=callback )
send_button.pack()


main.mainloop()
