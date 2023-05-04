
from tkinter import  N, Button, Frame, Text, Label, StringVar, END, INSERT, Toplevel, Entry, LEFT, RIGHT 
from tkinter import YES, BOTH

from tkinter.ttk import Combobox

import pgpy

class pgp_stuff:
    def __init__(self, frame, database, base_login=None):
        self.frame = frame
        self.database = database
        self.base_login = base_login
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
        
    

    def verify(self):

        #this ty/except will make it so there are not duplicats in the gui
        self.kill_children()

        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)

        self.verify_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="verify frame")
        self.verify_frame.pack(fill=BOTH, expand=YES)

        self.message_to_verify_text = Label(self.verify_frame, text="Message")
        self.message_to_verify_text.grid(column=0, row=0)

        self.message_to_verify_entery = Text(self.verify_frame, height = 25, width = 50)
        self.message_to_verify_entery.grid(column=0, row=1)

        
        self.public_key_verify_text = Label(self.verify_frame, text="Public Key")
        self.public_key_verify_text.grid(column=1, row=0)

        self.public_key_verify_entery = Text(self.verify_frame, height = 25, width = 50)
        self.public_key_verify_entery.grid(column=1, row=1)

        self.verify_button = Button(self.verify_frame, text="Verify", command=self.verify_function)
        self.verify_button.grid(column=3, row=0)
        
        self.verify_status = Label(self.verify_frame, text="Ready")
        self.verify_status.grid(column=4, row=0)

        self.verify_status.config(text="Ready")

    def verify_function(self):

        try:
            self.signd_message = pgpy.PGPMessage.from_blob(self.message_to_verify_entery.get("1.0","end-1c"))
            self.public_key, _ = pgpy.PGPKey.from_blob(self.public_key_verify_entery.get("1.0","end-1c"))

            if bool(self.public_key.verify(self.signd_message)):
                self.verify_status.config(text= "Verified")
            else:
                self.verify_status.config(text= "Bad")
        except:
            self.verify_status.config(text= "Bad")

        
    def encrypt(self):
        self.kill_children()

        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)

        self.encrypt_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="encrypt frame")
        self.encrypt_frame.pack(fill=BOTH, expand=YES)

        self.message_to_encrypt_text = Label(self.encrypt_frame, text="Message")
        self.message_to_encrypt_text.grid(column=0, row=0)

        self.message_to_encrypt_entery = Text(self.encrypt_frame, height = 25, width = 50)
        self.message_to_encrypt_entery.grid(column=0, row=1)

        
        self.public_key_encrypt_text = Label(self.encrypt_frame, text="Public Key")
        self.public_key_encrypt_text.grid(column=1, row=0)

        self.public_key_encrypt_entery = Text(self.encrypt_frame, height = 25, width = 50)
        self.public_key_encrypt_entery.grid(column=1, row=1)

        self.encrypt_button = Button(self.encrypt_frame, text="Encrypt", command=self.encrypt_function)
        self.encrypt_button.grid(column=3, row=0)

    def encrypt_function(self):
        self.pubkey, _ = pgpy.PGPKey.from_blob(self.public_key_encrypt_entery.get("1.0","end-1c"))
        self.message_to_encrypt = pgpy.PGPMessage.new(self.message_to_encrypt_entery.get("1.0","end-1c"))
        self.encrypted_message = self.pubkey.encrypt(self.message_to_encrypt)
        self.message_to_encrypt_entery.delete(1.0,END)
        self.message_to_encrypt_entery.insert(INSERT, self.encrypted_message)



    def decrypt(self):
        self.kill_children()
        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)

        self.decrypt_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="decrypt frame")
        self.decrypt_frame.pack(fill=BOTH, expand=YES)

        self.message_to_decrypt_text = Label(self.decrypt_frame, text="Message")
        self.message_to_decrypt_text.grid(column=0, row=0)

        self.message_to_decrypt_entery = Text(self.decrypt_frame, height = 25, width = 50)
        self.message_to_decrypt_entery.grid(column=0, row=1)

        self.public_key_decrypt_text = Label(self.decrypt_frame, text="Private Key")
        self.public_key_decrypt_text.grid(column=1, row=0)
        
        self.public_key_decrypt_text = Combobox(self.decrypt_frame, values=self.database.get_entries_with_private_keys(self.temp_password), state="readonly")
        self.public_key_decrypt_text.grid(column=1, row=1, sticky=N)

        self.decrypt_button = Button(self.decrypt_frame, text="decrypt", command=self.decrypt_pgp)
        self.decrypt_button.grid(column=3, row=0)

    def decrypt_pgp(self):
        private_key, pgp_password = self.database.get_private_key_and_passphrase_by_refrance(self.temp_password, self.public_key_decrypt_text.get())
        
        self.privkey, _ = pgpy.PGPKey.from_blob(private_key)
        with self.privkey.unlock(pgp_password) as ukey:
            self.message_to_decrypt = pgpy.PGPMessage.from_blob(self.message_to_decrypt_entery.get("1.0","end-1c"))
            self.decrypted_massage = ukey.decrypt(self.message_to_decrypt).message 
            self.message_to_decrypt_entery.delete(1.0,END)
            self.message_to_decrypt_entery.insert(INSERT, self.decrypted_massage)

    def sign(self):
        self.kill_children()
        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)

        self.sign_frame = Frame(self.frame, highlightbackground="green", highlightthickness=2, name="sign frame")
        self.sign_frame.pack(fill=BOTH, expand=YES)

        self.message_to_sign_text = Label(self.sign_frame, text="Message")
        self.message_to_sign_text.grid(column=0, row=0)

        self.message_to_sign_entery = Text(self.sign_frame, height = 25, width = 50)
        self.message_to_sign_entery.grid(column=0, row=1)

        self.private_key_sign_text = Label(self.sign_frame, text="Private Key")
        self.private_key_sign_text.grid(column=1, row=0)
        
        self.private_key_sign_combo = Combobox(self.sign_frame, values=self.database.get_entries_with_private_keys(self.temp_password), state="readonly")
        self.private_key_sign_combo.grid(column=1, row=1, sticky=N)

        self.sign_button = Button(self.sign_frame, text="sign", command=self.sign_function)
        self.sign_button.grid(column=3, row=0)

    def sign_function(self):
        self.plain_text_massage = self.message_to_sign_entery.get("1.0","end-1c")

        private_key, pgp_password = self.database.get_private_key_and_passphrase_by_refrance(self.temp_password, self.private_key_sign_combo.get())
        
        self.privkey, _ = pgpy.PGPKey.from_blob(private_key)
        with self.privkey.unlock(pgp_password) as ukey:
            self.massage_to_sign = self.message_to_sign_entery.get("1.0","end-1c")
            self.detached_signiture = ukey.sign(self.massage_to_sign)

            self.attached_signed_message = f"-----BEGIN PGP SIGNED MESSAGE-----\n{self.massage_to_sign}\n{str(self.detached_signiture)}"
            self.message_to_sign_entery.delete(1.0,END)
            self.message_to_sign_entery.insert(INSERT, self.attached_signed_message)
