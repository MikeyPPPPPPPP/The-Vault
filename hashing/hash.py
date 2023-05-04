from tkinter import  N, Button, Frame, Text, Label, StringVar, END, INSERT
from tkinter import YES, BOTH

from tkinter.ttk import Combobox

import hashlib

class hash_stuff:
    def __init__(self, frame):
        self.frame = frame

    def kill_children(self):
        #kills the child frames of the main frame
        for child in self.frame.winfo_children():
            child.destroy()

    def hash_me(self):
        self.kill_children()
        self.hash_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2)
        self.hash_frame.pack(fill=BOTH, expand=YES)

        self.message_to_hash_text = Label(self.hash_frame, text="Message")
        self.message_to_hash_text.grid(column=0, row=0)

        self.message_to_hash_entery = Text(self.hash_frame, height = 25, width = 50)
        self.message_to_hash_entery.grid(column=0, row=1)

        self.message_to_hash_text_2 = Label(self.hash_frame, text="Hash algorithm")
        self.message_to_hash_text_2.grid(column=1, row=0)

        self.combobox_hash = Combobox(self.hash_frame, state="readonly")
        self.combobox_hash['values']=('md5','sha1','sha256', 'sha224','sha384', 'sha512')
        self.combobox_hash.current(0)
        self.combobox_hash.grid(column=1, row=1, sticky=N)

        self.hashed_message_text = Label(self.hash_frame, text="Hash")
        self.hashed_message_text.grid(column=3, row=0)

        self.message_hashed_entery = Text(self.hash_frame, height = 5, width = 40)
        self.message_hashed_entery.grid(column=3, row=1, sticky=N)

        self.hash_button = Button(self.hash_frame, text="Hash", command=self.hash_the_one)
        self.hash_button.grid(column=1, row=2)

    def hash_the_one(self):
        self.hash_algor = self.combobox_hash.get()

        self.message_hashed_entery.delete(1.0,END)
        if self.hash_algor == 'md5':
            temp = hashlib.md5(str(self.message_to_hash_entery.get("1.0","end-1c")).encode())
            self.message_hashed_entery.insert(INSERT, temp.hexdigest())
        if self.hash_algor == 'sha1':
            temp = hashlib.sha1(str(self.message_to_hash_entery.get("1.0","end-1c")).encode())
            self.message_hashed_entery.insert(INSERT, temp.hexdigest())
        if self.hash_algor == 'sha256':
            temp = hashlib.sha256(str(self.message_to_hash_entery.get("1.0","end-1c")).encode())
            self.message_hashed_entery.insert(INSERT, temp.hexdigest())
        if self.hash_algor == 'sha224':
            temp = hashlib.sha224(str(self.message_to_hash_entery.get("1.0","end-1c")).encode())
            self.message_hashed_entery.insert(INSERT, temp.hexdigest())
        if self.hash_algor == 'sha384':
            temp = hashlib.sha384(str(self.message_to_hash_entery.get("1.0","end-1c")).encode())
            self.message_hashed_entery.insert(INSERT, temp.hexdigest())
        if self.hash_algor == 'sha512':
            temp = hashlib.sha512(str(self.message_to_hash_entery.get("1.0","end-1c")).encode())
            self.message_hashed_entery.insert(INSERT, temp.hexdigest())