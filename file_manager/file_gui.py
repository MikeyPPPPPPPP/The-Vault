from tkinter import filedialog as fd

from tkinter import  E, W, Button, Frame, Text, Label, Entry, Toplevel, RIGHT, LEFT
from tkinter import YES, BOTH
from tkinter.ttk import Combobox
import os
from PIL import Image, ImageTk
import io

class file_manager:
    def __init__(self, frame, database, base_login=None):
        self.frame = frame
        self.temp_file = None
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

    def get_paths(self):
        filename = fd.askopenfilenames()
        self.temp_file = filename



    def add_files(self):
        self.kill_children()

        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)




        self.add_file_frame = Frame(self.frame)
        self.add_file_frame.pack(fill=BOTH, expand=YES)


        self.small_frame = Frame(self.add_file_frame)
        self.small_frame.grid(column=0, row=1, sticky=W)

        self.refrance_label = Label(self.small_frame, text="Refrence")
        self.refrance_label.grid(column=0, row=0, sticky=W)

        self.refrance_entry = Entry(self.small_frame)
        self.refrance_entry.grid(column=1, row=0)


        self.choose_file = Button(self.small_frame, text="choose file", command=self.get_paths)
        self.choose_file.grid(column=0, row=1, sticky=W)

        self.submit_file = Button(self.small_frame, text="Submit", command=self.process_given_files)
        self.submit_file.grid(column=1, row=1, sticky=E)

    def process_given_files(self):
        """this will check the file list and process each file into the database"""
        if self.temp_file == None:
            #open a dialog that says nofiles in qeue
            pass
        #check that a refrence is added befor moving on

        temp_dict_to_give_to_function = {"refrence":self.refrance_entry.get(), "filename":self.temp_file[0]}

        self.database.add_a_file(self.temp_password, temp_dict_to_give_to_function)
        self.temp_file = None
        self.recover_file()



    def recover_file(self):
        self.kill_children()

        self.recover_file_frame = Frame(self.frame)
        self.recover_file_frame.pack(fill=BOTH, expand=YES)

        self.pick_file_label = Label(self.recover_file_frame, text="choose")
        self.pick_file_label.grid(column=0, row=0)

        self.file_combo = Combobox(self.recover_file_frame, values=self.database.retreve_file_refrences(), state="readonly")
        self.file_combo.grid(column=1, row=0)

        self.recover = Button(self.recover_file_frame, text = "Recover", command=self.recover_file_to_computer)
        self.recover.grid(column=0, row=1)


        self.small_frame = Frame(self.recover_file_frame)
        self.small_frame.grid(column=1, row=1, sticky=W)

        self.view_file = Button(self.small_frame, text = "Delete", command=self.delete_file_by_refrance_buttom_command)
        self.view_file.grid(column=0, row=0, sticky=W)

        self.view_file = Button(self.small_frame, text = "View Image", command = self.veiw_image)
        self.view_file.grid(column=1, row=0, sticky=W)

    def recover_file_to_computer(self):
        refr = self.file_combo.get()
        dict_data = self.database.get_file_data_by_refrance(refr, self.temp_password)
        filename = dict_data["filename"]+"."+dict_data["file_extention"]

        with open(filename,"wb") as file:
            file.write(bytes(dict_data["data"]))
        self.add_files()

    def delete_file_by_refrance_buttom_command(self):
        refr = self.file_combo.get()
        self.database.delete_file_data_by_refrance(refr)
        self.add_files()

    def veiw_image(self):
        refr = self.file_combo.get()
        dict_data = self.database.get_file_data_by_refrance(refr, self.temp_password)
        if dict_data["file_extention"] in ["png", "jpeg", "prm", "gif", "tiff", "bmp"]:
            image_data = dict_data["data"]
            image = Image.open(io.BytesIO(image_data))
            width, height = image.size
            image_frame = Toplevel(self.recover_file_frame)
            image_frame.geometry(str(width)+"x"+str(height))

            test = ImageTk.PhotoImage(image)
            label = Label(image_frame, image=test)
            label.image = test

                # Position image
            label.place(x=0, y=0)








