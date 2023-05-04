
from tkinter import  E, W, NW, S, Button, Frame, Text, Label, END, INSERT, Checkbutton, Toplevel, RIGHT, LEFT, Entry
from tkinter import YES, BOTH, IntVar


from tkinter.ttk import Combobox
import pyperclip
"""
1. login
2. show/add to
3. if show, select the one you want with a combobox
4. if add, get the entries and add them to the database
"""
#show via table
class password_manager:
    def __init__(self, frame, database, base_login=None):
        self.frame = frame
        self.database = database
        self.base_login = base_login
        self.temp_dict = {'refrence_text': '', 'site_text': '', 'username_text': '', 'password_text': '', 'pin_text': '', 'email_text': '', 'phone_number_text': '', 'note_text': '', 'public_text': '', 'passphrase_text':'', 'private_text': ''}

        self.temp_password = None
        if self.base_login != None:
            self.temp_password = self.base_login.password

    def login_exec(self, event):
        temp_password = bytes(self.login_password_input.get().encode())

        if self.database.test_password(temp_password):
            self.temp_password = bytes(self.login_password_input.get().encode())
            self.login_frame.destroy()
        else:
            self.frame.destroy()


    def login(self):
        self.login_frame = Toplevel(self.frame)
        self.login_frame.geometry("300x50")
        
        self.login_password_text = Label(self.login_frame, text="Password")
        self.login_password_text.pack(side = LEFT)
        
        self.login_password_input = Entry(self.login_frame, bd =5)
        self.login_password_input.pack(side = RIGHT)
        
        self.login_frame.bind('<Return>', self.login_exec)

    def kill_children(self):
        #kills the child frames of the main frame
        for child in self.frame.winfo_children():
            child.destroy()

    def add_password(self):
        self.kill_children()
        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)

        self.add_password_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="add_password frame")
        self.add_password_frame.pack(fill=BOTH, expand=YES)

        self.add_password_top_label = Label(self.add_password_frame, text="Add a Password")
        self.add_password_top_label.grid(column=1, row=0)

        self.refrence_label = Label(self.add_password_frame, text="Refrence")
        self.refrence_label.grid(column=0, row=1, sticky=W)
        self.refrence_text = Text(self.add_password_frame, height = 1, width = 95)
        self.refrence_text.grid(column=1, row=1)
        self.refrence_text.insert('1.0', self.temp_dict["refrence_text"])

        self.site_label = Label(self.add_password_frame, text="Site url")
        self.site_label.grid(column=0, row=2, sticky=W)
        self.site_text = Text(self.add_password_frame, height = 1, width = 95)
        self.site_text.grid(column=1, row=2)
        self.site_text.insert('1.0', self.temp_dict["site_text"])

        self.username_label = Label(self.add_password_frame, text="Username")
        self.username_label.grid(column=0, row=3, sticky=W)
        self.username_text = Text(self.add_password_frame, height = 1, width = 95)
        self.username_text.grid(column=1, row=3)
        self.username_text.insert('1.0', self.temp_dict["username_text"])

        self.password_label = Label(self.add_password_frame, text="Password")
        self.password_label.grid(column=0, row=4, sticky=W)
        self.password_text = Text(self.add_password_frame, height = 1, width = 95)
        self.password_text.grid(column=1, row=4)
        self.password_text.insert('1.0', self.temp_dict["password_text"])

        self.pin_label = Label(self.add_password_frame, text="Pin")
        self.pin_label.grid(column=0, row=5, sticky=W)
        self.pin_text = Text(self.add_password_frame, height = 1, width = 95)
        self.pin_text.grid(column=1, row=5)
        self.pin_text.insert('1.0', self.temp_dict["pin_text"])

        self.email_label = Label(self.add_password_frame, text="Email")
        self.email_label.grid(column=0, row=6, sticky=W)
        self.email_text = Text(self.add_password_frame, height = 1, width = 95)
        self.email_text.grid(column=1, row=6)
        self.email_text.insert('1.0', self.temp_dict["email_text"])

        self.phone_number_label = Label(self.add_password_frame, text="Phone number")
        self.phone_number_label.grid(column=0, row=7, sticky=W)
        self.phone_number_text = Text(self.add_password_frame, height = 1, width = 95)
        self.phone_number_text.grid(column=1, row=7)
        self.phone_number_text.insert('1.0', self.temp_dict["phone_number_text"])

        self.note_label = Label(self.add_password_frame, text="Note")
        self.note_label.grid(column=0, row=8, sticky=NW)
        self.note_text = Text(self.add_password_frame, height = 11, width = 95)
        self.note_text.grid(column=1, row=8)
        self.note_text.insert('1.0', self.temp_dict["note_text"])


        self.var1 = IntVar()
        self.public_key_box_text = Checkbutton(self.add_password_frame, text="Asymmetric Keys", variable=self.var1, onvalue=1, offvalue=0)
        self.public_key_box_text.grid(column=1, row=9, sticky=W)


        self.continue_button = Button(self.add_password_frame, text="Continue ->", command=self.get_password_data_from_add_a_password)
        self.continue_button.grid(column=3, row=15, sticky=S)

    def get_password_data_from_add_a_password(self):

        self.temp_dict["refrence_text"]=self.refrence_text.get("1.0","end-1c")
        self.temp_dict["site_text"]=self.site_text.get("1.0","end-1c")
        self.temp_dict["username_text"]=self.username_text.get("1.0","end-1c")
        self.temp_dict["password_text"]=self.password_text.get("1.0","end-1c")
        self.temp_dict["pin_text"]=self.pin_text.get("1.0","end-1c")
        self.temp_dict["email_text"]=self.email_text.get("1.0","end-1c")
        self.temp_dict["phone_number_text"]=self.phone_number_text.get("1.0","end-1c")
        self.temp_dict["note_text"]=self.note_text.get("1.0","end-1c")

        temp_asym = self.var1.get()
        if temp_asym == 1:
            self.get_public_private()
        else:    
            self.add_password_data_to_database()






    def get_public_private(self):

        self.kill_children()

        self.add_keys_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="add_password frame")
        self.add_keys_frame.pack(fill=BOTH, expand=YES)


        self.public_label = Label(self.add_keys_frame, text="Public Key")
        self.public_label.grid(column=0, row=0)
        self.public_text = Text(self.add_keys_frame, height = 25, width = 50)
        self.public_text.grid(column=0, row=2)
        self.public_text.insert('1.0', self.temp_dict["public_text"])

        self.private_label = Label(self.add_keys_frame, text="Private Key")
        self.private_label.grid(column=1, row=0)
        self.private_text = Text(self.add_keys_frame, height = 25, width = 50)
        self.private_text.grid(column=1, row=2)
        self.private_text.insert('1.0', self.temp_dict["private_text"])



        self.passphrase_frame = Frame(self.add_keys_frame)
        self.passphrase_frame.grid(column=1, row=3, sticky=W)

        self.passphrase_label = Label(self.passphrase_frame, text="PassPhrase")
        self.passphrase_label.grid(column=0, row=0, sticky=W)

        self.passphrase_text = Text(self.passphrase_frame, height = 1, width = 30)
        self.passphrase_text.grid(column=1, row=0, sticky=W)

        self.back_button = Button(self.add_password_frame, text="<- Back", command=self.back_button)
        self.back_button.grid(column=3, row=3, sticky=E)

        self.finish_button = Button(self.add_password_frame, text="Finish ->", command=self.add_password_data_to_database)
        self.finish_button.grid(column=4, row=3, sticky=W)

    def back_button(self):
        self.get_public_and_private_keys_from_gui()
        self.add_password()

    def get_public_and_private_keys_from_gui(self):
        self.temp_dict["public_text"] =  self.public_text.get("1.0","end-1c")
        self.temp_dict["private_text"] =  self.private_text.get("1.0","end-1c")
        self.temp_dict["passphrase_text"] =  self.passphrase_text.get("1.0","end-1c")

        
        
        
    def add_password_data_to_database(self):
        self.get_public_and_private_keys_from_gui()
        print(self.temp_dict)
        raw_data = {"refrence":self.temp_dict["refrence_text"], "site_url":self.temp_dict["site_text"], "username":self.temp_dict["username_text"], "password":self.temp_dict["password_text"], "pin":self.temp_dict["pin_text"], "email":self.temp_dict["email_text"], "phonenumber":self.temp_dict["phone_number_text"], "public_key":self.temp_dict["public_text"], "private_key":self.temp_dict["private_text"],"pgp_password":self.temp_dict["passphrase_text"], "note":self.temp_dict["note_text"]}
        #this line is cool; https://stackoverflow.com/questions/9442724/how-can-i-use-if-else-in-a-dictionary-comprehension
        finalized_data = {x:(y if y != '' else 'default data') for x,y in raw_data.items()}
        self.database.add_a_password(self.temp_password, finalized_data)
        print(finalized_data)
        self.temp_dict = {'refrence_text': '', 'site_text': '', 'username_text': '', 'password_text': '', 'pin_text': '', 'email_text': '', 'phone_number_text': '', 'note_text': '', 'public_text': '', 'passphrase_text':'', 'private_text': ''}
        self.choose_password()
        

   
    def view_password(self, refr):
        #use pyperclip to copy the public or private key to the clipboard
        self.kill_children()
        password_data = self.database.get_password_data_by_refrance(refr, self.temp_password)#dict

        self.view_password_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="add_password frame")
        self.view_password_frame.pack(fill=BOTH, expand=YES)

        self.var0 = IntVar(value=0)
        self.all_show = Checkbutton(self.view_password_frame, variable=self.var0)
        self.all_show.grid(column=0, row=0, sticky=W)
        self.add_password_top_label = Label(self.view_password_frame, text="Show All")
        self.add_password_top_label.grid(column=1, row=0, sticky=W)
        

        self.var1 = IntVar()
        self.site_show = Checkbutton(self.view_password_frame, variable=self.var1)
        self.site_show.grid(column=0, row=1, sticky=W)
        self.site_label = Label(self.view_password_frame, text="Site url")
        self.site_label.grid(column=1, row=1, sticky=W)
        self.site_text = Text(self.view_password_frame, height = 1, width = 95)
        self.site_text.grid(column=2, row=1)
        self.site_text.insert('1.0', password_data["site_url"])

        self.var2 = IntVar()
        self.username_show = Checkbutton(self.view_password_frame, variable=self.var2)
        self.username_show.grid(column=0, row=2, sticky=W)
        self.username_label = Label(self.view_password_frame, text="Username")
        self.username_label.grid(column=1, row=2, sticky=W)
        self.username_text = Text(self.view_password_frame, height = 1, width = 95)
        self.username_text.grid(column=2, row=2)
        self.username_text.insert('1.0', password_data["username"])

        self.var3 = IntVar()
        self.password_show = Checkbutton(self.view_password_frame, variable=self.var3)
        self.password_show.grid(column=0, row=3, sticky=W)
        self.password_label = Label(self.view_password_frame, text="Password")
        self.password_label.grid(column=1, row=3, sticky=W)
        self.password_text = Text(self.view_password_frame, height = 1, width = 95)
        self.password_text.grid(column=2, row=3)
        self.password_text.insert('1.0', password_data["password"])


        self.var4 = IntVar()
        self.pin_show = Checkbutton(self.view_password_frame, variable=self.var4)
        self.pin_show.grid(column=0, row=4, sticky=W)
        self.pin_label = Label(self.view_password_frame, text="Pin")
        self.pin_label.grid(column=1, row=4, sticky=W)
        self.pin_text = Text(self.view_password_frame, height = 1, width = 95)
        self.pin_text.grid(column=2, row=4)
        self.pin_text.insert('1.0', password_data["pin"])

        self.var5 = IntVar()
        self.email_show = Checkbutton(self.view_password_frame, variable=self.var5)
        self.email_show.grid(column=0, row=5, sticky=W)
        self.email_label = Label(self.view_password_frame, text="Email")
        self.email_label.grid(column=1, row=5, sticky=W)
        self.email_text = Text(self.view_password_frame, height = 1, width = 95)
        self.email_text.grid(column=2, row=5)
        self.email_text.insert('1.0', password_data["email"])

        self.var6 = IntVar()
        self.phone_number_show = Checkbutton(self.view_password_frame, variable=self.var6)
        self.phone_number_show.grid(column=0, row=6, sticky=W)
        self.phone_number_label = Label(self.view_password_frame, text="Phone number")
        self.phone_number_label.grid(column=1, row=6, sticky=W)
        self.phone_number_text = Text(self.view_password_frame, height = 1, width = 95)
        self.phone_number_text.grid(column=2, row=6)
        self.phone_number_text.insert('1.0', password_data["phonenumber"])

        self.var7 = IntVar()
        self.note_number_show = Checkbutton(self.view_password_frame, variable=self.var7)
        self.note_number_show.grid(column=0, row=7, sticky=NW)
        self.note_label = Label(self.view_password_frame, text="Note")
        self.note_label.grid(column=1, row=7, sticky=NW)
        self.note_text = Text(self.view_password_frame, height = 11, width = 95)
        self.note_text.grid(column=2, row=7)
        self.note_text.insert('1.0', password_data["note"])

        self.public_key_button = Button(self.view_password_frame, text="Public", command=lambda:pyperclip.copy(password_data["public_key"]))
        self.public_key_button.grid(column=1, row=8)

        self.private_key_button = Button(self.view_password_frame, text="Private", command=lambda:pyperclip.copy(password_data["private_key"]))
        self.private_key_button.grid(column=1, row=9)

    def choose_password(self):

        self.kill_children()
        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)
        
        self.pick_password_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="add_password frame")
        self.pick_password_frame.pack(fill=BOTH, expand=YES)

        self.password_combo = Combobox(self.pick_password_frame, values=self.database.retreve_password_refrences(), state="readonly")
        self.password_combo.grid(column=0, row=0)

        self.select_password = Button(self.pick_password_frame, text="View", command=lambda: self.view_password(self.password_combo.get()))
        self.select_password.grid(column=2, row=0)

        self.delete_password = Button(self.pick_password_frame, text="Delete", command=lambda: self.database.delete_password_data_by_refrance(self.password_combo.get()))
        self.delete_password.grid(column=3, row=0)
