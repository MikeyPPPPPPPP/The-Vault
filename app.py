

import tkinter as tk
from tkinter import Menu, Frame
from tkinter import YES, BOTH

from pgp.pgp_page import pgp_stuff
from hashing.hash import hash_stuff
from password_manager.password_gui import password_manager
from file_manager.file_gui import file_manager
from options.opt import option_panal
from login import login

#databse stuff
from encryption.machine import Database_equiptment

"""
1. delete
2. update
"""

'''
menu shows at the top of the screen
'''



class passwordGUI(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.pack()
		self.master.title("The Vault")

		self.database = Database_equiptment("sqlite:///fhritp.db")
		self.database.create_database()
		#self.database.fresh_and_clean()
		
		self.log = login(self.master, self.database)
		self.log.login()
		self.master.wait_window(self.log.login_frame)

		self.master.geometry("900x400")
		#this puts the gui more in the middle
		self.master.eval('tk::PlaceWindow . center')
		
		#the main fram to build stuff in
		self.main_Frame = Frame(self.master, highlightbackground="blue", highlightthickness=2)
		self.main_Frame.pack(fill=BOTH, expand=YES) 


		self.setup_mods()
		self.make_menu()

		#temp
		self.pgp_frame.verify()

	def make_menu(self):
		self.main_menu = Menu(self.master)
		self.master.config(menu=self.main_menu)

		self.pgp = Menu(self.main_menu, tearoff=0)
		self.pgp.add_command(label="Decrypt", command=self.pgp_frame.decrypt)		
		self.pgp.add_command(label="Encrypt", command=self.pgp_frame.encrypt)	
		self.pgp.add_command(label="Verify", command=self.pgp_frame.verify)	
		self.pgp.add_command(label="Sign", command=self.pgp_frame.sign)	
		self.main_menu.add_cascade(label="PGP", menu=self.pgp)
	
		self.hashing = Menu(self.main_menu, tearoff=0)
		self.hashing.add_command(label="basic", command=self.hash_frame.hash_me)		
		self.main_menu.add_cascade(label="Hashing", menu=self.hashing)

		self.password_manager = Menu(self.main_menu, tearoff=0)
		self.password_manager.add_command(label="Add", command=self.password_frame.add_password)
		self.password_manager.add_command(label="Veiw", command=self.password_frame.choose_password)
		self.main_menu.add_cascade(label="Password Manager", menu=self.password_manager)

		self.file_manages = Menu(self.main_menu, tearoff=0)
		self.file_manages.add_command(label="Add", command=self.file_manager_frame.add_files)	
		self.file_manages.add_command(label="View", command=self.file_manager_frame.recover_file)	
		self.main_menu.add_cascade(label="File Manager", menu=self.file_manages)

		self.options = Menu(self.main_menu, tearoff=0)
		self.options.add_command(label="settings", command=self.option_frame.main_option_frame)	
		self.main_menu.add_cascade(label="Options", menu=self.options)

	def setup_mods(self):
		if self.database.get_paranoid_setting() == 0:
			self.pgp_frame = pgp_stuff(self.main_Frame, self.database, self.log)
			self.hash_frame = hash_stuff(self.main_Frame) 
			self.password_frame = password_manager(self.main_Frame, self.database, self.log)
			self.file_manager_frame = file_manager(self.main_Frame, self.database, self.log)
			self.option_frame = option_panal(self.main_Frame, self.database)
		else:
			self.pgp_frame = pgp_stuff(self.main_Frame, self.database)
			self.hash_frame = hash_stuff(self.main_Frame) 
			self.password_frame = password_manager(self.main_Frame, self.database)
			self.file_manager_frame = file_manager(self.main_Frame, self.database)
			self.option_frame = option_panal(self.main_Frame, self.database)

		
root = tk.Tk()

app = passwordGUI(root)
app.mainloop()



