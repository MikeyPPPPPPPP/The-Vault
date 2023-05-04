#add a password persistance option
#delete file after storeing it


from tkinter import  W, Frame, Checkbutton, IntVar, Toplevel, LEFT, RIGHT, Entry, Label
from tkinter import YES, BOTH


class option_panal:
    def __init__(self, frame, database):
        self.frame = frame
        self.database = database

    def login_exec(self, event):
        temp_password = bytes(self.login_password_input.get().encode())

        if self.database.test_password(temp_password):
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
        
    def main_option_frame(self):
        self.kill_children()
        if self.database.get_paranoid_setting() == 1:
            self.login()
            self.frame.wait_window(self.login_frame)

        self.option_frame = Frame(self.frame, name="option frame")
        self.option_frame.pack(fill=BOTH, expand=YES)

        self.var1 = IntVar()
        self.var1.set(self.database.get_paranoid_setting())
        self.option1 = Checkbutton(self.option_frame, text="Paranoid option off",variable=self.var1, onvalue=1, offvalue=0, command=self.database.change_paranoid_setting)
        self.option1.grid(column=0, row=0, sticky=W)

        self.var2 = IntVar(value=self.database.get_delete_setting)
        self.var2.set(self.database.get_delete_setting())
        self.option2 = Checkbutton(self.option_frame, text="Delete file after storeing",variable=self.var2, onvalue=1, offvalue=0, command=self.database.change_delete_setting)
        self.option2.grid(column=0, row=2, sticky=W)

        self.var3 = IntVar()
        self.var3.set(0)
        self.option3 = Checkbutton(self.option_frame, text="Currupt database after 3 falied attempts",variable=self.var3, onvalue=1, offvalue=0)
        self.option3.grid(column=0, row=3, sticky=W)


        self.var4 = IntVar()
        self.var4.set(0)
        self.option4 = Checkbutton(self.option_frame, text="Log falied attempts",variable=self.var4, onvalue=1, offvalue=0)
        self.option4.grid(column=0, row=4, sticky=W)

        self.var6 = IntVar()
        self.var6.set(0)
        self.option6 = Checkbutton(self.option_frame, text="Take a picture on attempt",variable=self.var6, onvalue=1, offvalue=0)
        self.option6.grid(column=0, row=4, sticky=W)

        self.var5 = IntVar()
        self.var5.set(0)
        self.option5 = Checkbutton(self.option_frame, text="Make Backup",variable=self.var5, onvalue=1, offvalue=0)
        self.option5.grid(column=0, row=5, sticky=W)

    