from tkinter import Entry, LEFT, RIGHT, Label, Toplevel


class login:
    def __init__(self, frame, database):
        self.frame = frame
        self.database = database
        self.password = None

    def login_exec(self, event):
        temp_password = bytes(self.login_password_input.get().encode())

        if self.database.test_password(temp_password):
            self.password = temp_password
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