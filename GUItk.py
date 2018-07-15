import tkinter as t
import sys
# import main as m


class App:
    # define main properties
    page = 0
    height = 600
    width = 1024
    usernames = list(open("accounts.txt", "r"))
    passwords = list(open("passwords.txt", "r"))

    def __init__(self):
        self.root = t.Tk()
        self.root.config(bg="light grey")
        self.root.title("T.E.S.T.")
        self.root.pack_propagate(0)
        self.root.resizable(0, 0)
        self.root.geometry('%(a)d' % {'a': self.width} + 'x' + '%(b)d' % {'b': self.height})
        self.root.bind('<Escape>', self.stop)
        self.root.update()
        self.generate_objects()
        self.root.mainloop()

    """Function to generate pages"""
    def generate_objects(self, *args):
        switcher = {
            0: self.generate_login,
            1: self.generate_page_one,
            2: self.generate_page_two,
            3: self.generate_page_three,
            4: self.generate_page_four,
            5: self.generate_new_account
        }
        switcher[self.page]()

    """Function to switch pages"""
    def change_page(self, number):
        self.page = number
        for kid in self.root.winfo_children():
            kid.destroy()
        self.generate_objects()

    """Login function"""
    def login(self, username, password):
        if username == 'admin' and password == 'admin':
            print('Username: ' + username)
            print('Password: ' + password)
            self.change_page(1)
        else:
            error_frame = t.Frame(self.root, bg="light grey")
            error_frame.place(relheight=0.05, relwidth=0.233, relx=0.4, rely=0.55)
            error_text = t.Label(error_frame, fg="red", bg="light grey", text="Username or password incorrect")
            error_text.pack(side="bottom", fill="both", expand="true")
            print('Username or password incorrect, access denied')

    def generate_login(self):
        # create upper frame with text
        login_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() / 4))
        login_frame.pack(side="top", fill="x", expand="false")
        login_frame.update()
        login_frame.propagate(0)
        login_text = t.Label(login_frame, bg="grey", text="Login")
        login_text.pack(side="bottom", fill="both", expand="true")
        # create entry box
        entry_frame = t.Frame(self.root, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg="light grey")
        entry_frame.pack(side="top", expand="false")
        entry_frame.update()
        entry_frame.propagate(0)
        # label and box for username
        user_label = t.Label(entry_frame, bg="light grey", text="Username:")
        user_label.place(relheight=0.1, relwidth=0.4, relx=0.1, rely=0.4)
        username_box = t.Entry(entry_frame)
        username_box.place(relheight=0.1, relwidth=0.4, relx=0.5, rely=0.4)
        # label and box for password
        pwd_label = t.Label(entry_frame, bg="light grey", text="Password:")
        pwd_label.place(relheight=0.1, relwidth=0.4, relx=0.1, rely=0.5)
        password_box = t.Entry(entry_frame, show="*")
        password_box.place(relheight=0.1, relwidth=0.4, relx=0.5, rely=0.5)
        # create login button
        login_button = t.Button(entry_frame, text="Login", bg="dark grey",
                                command=lambda: self.login(username=username_box.get(), password=password_box.get()))
        login_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.8)

        test_button = t.Button(self.root, text="Create new account", bg="dark grey",
                               command=lambda: self.change_page(5))
        test_button.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.9)

        # testing purposes
        array_button = t.Button(self.root, text="Print array", bg="dark grey",
                                command=lambda: [print(self.usernames),
                                                 print(self.passwords)])
        array_button.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.8)

    def generate_new_account(self):
        # create upper frame with text
        account_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() / 4))
        account_frame.pack(side="top", fill="x", expand="false")
        account_frame.update()
        account_frame.propagate(0)
        login_text = t.Label(account_frame, bg="grey", text="Account creation")
        login_text.pack(side="bottom", fill="both", expand="true")
        # create entry box
        input_frame = t.Frame(self.root, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg="light grey")
        input_frame.pack(side="top", expand="false")
        input_frame.update()
        input_frame.propagate(0)
        # label and box for username
        user_label = t.Label(input_frame, bg="light grey", text="Enter new username:")
        user_label.place(relheight=0.1, relwidth=0.4, relx=0.1, rely=0.4)
        username_box = t.Entry(input_frame)
        username_box.place(relheight=0.1, relwidth=0.4, relx=0.5, rely=0.4)
        # label and box for password
        pwd_label = t.Label(input_frame, bg="light grey", text="Enter new password:")
        pwd_label.place(relheight=0.1, relwidth=0.4, relx=0.1, rely=0.5)
        password_box = t.Entry(input_frame, show="*")
        password_box.place(relheight=0.1, relwidth=0.4, relx=0.5, rely=0.5)
        # create login button
        create_button = t.Button(input_frame, text="Create", bg="dark grey",
                                 command=lambda: [self.usernames.append(username_box.get()),
                                                  self.passwords.append(password_box.get()),
                                                  self.change_page(0)])
        create_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.8)

    def generate_page_one(self):
        description = "Here will be the description of the machine..."
        frame_height = int(self.root.winfo_height() / 2)
        bottom_frame = t.Frame(self.root, width=self.root.winfo_width(), height=frame_height, bg="white")
        bottom_frame.pack(side="bottom", fill="x", expand="false")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        top_text = t.Label(self.root, bg="grey", text=description)
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        bottom_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                 fg="white",
                                 text="Start", command=lambda: self.change_page(2))
        bottom_button.update()
        bottom_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.45)

    def generate_page_two(self):
        title = "Pre-Measurement"
        # begin top bar of screen
        top_bar = t.Frame(self.root, bg="white", height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)
        # begin text and button of top bar
        top_text = t.Label(top_bar, bg="white", text=title)
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground="dark grey", activeforeground="white", bg="black", fg="white",
                               text="Back", command=lambda: self.change_page(1))
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        # begin upper part of screen
        instruction_bar = t.Frame(self.root, bg="grey", height=int(self.root.winfo_height() * 0.3))
        instruction_bar.pack(fill="x")
        instruction_text = t.Label(instruction_bar, bg="grey", text="Instructions for use...")
        instruction_text.place(relheight=1, relwidth=1)
        # begin lower part of screen
        bottom_frame = t.Frame(self.root, bg="white")
        bottom_frame.pack(side="bottom", fill="both", expand="true")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        measure_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                  fg="green", disabledforeground="red", state="disabled", text="Measure",
                                  command=lambda: self.change_page(3))
        measure_button.update()
        measure_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)
        # make precondition button update the properties of the measure button
        precond_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                  fg="white", text="Pre-condition check",
                                  command=lambda: measure_button.config(state="normal"))
        precond_button.update()
        precond_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.3)

    def generate_page_three(self):
        title = "Measurement"
        # begin top bar of screen
        top_bar = t.Frame(self.root, bg="white", height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)
        # begin text and button of top bar
        top_text = t.Label(top_bar, bg="white", text=title)
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground="dark grey", activeforeground="white", bg="black", fg="white",
                               text="Back", command=lambda: self.change_page(2))
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        # begin upper part of screen
        loading_bar = t.Frame(self.root, bg="grey", height=int(self.root.winfo_height() * 0.3))
        loading_bar.pack(fill="x")
        loading_text = t.Label(loading_bar, bg="grey", text="Loading...")
        loading_text.place(relheight=1, relwidth=1)
        # begin lower part of screen
        bottom_frame = t.Frame(self.root, bg="white")
        bottom_frame.pack(side="bottom", fill="both", expand="true")
        bottom_frame.update()
        bottom_frame.propagate(0)

        # temporary button, testing purposes only
        temp_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                               fg="white", state="normal", text="Next", command=lambda: self.change_page(4))
        temp_button.update()
        temp_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)
        # end temporary button

    def generate_page_four(self):
        title = "Results"
        # begin top bar of screen with text
        top_bar = t.Frame(self.root, bg="white", height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.propagate(0)
        top_text = t.Label(top_bar, bg="white", text=title)
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()

        # begin left part of screen
        left_col = t.Frame(self.root, bg="white", width=int(self.root.winfo_width() / 2))
        left_col.pack(side="left", fill="y", expand="false")
        left_col.update()
        left_col.propagate(0)
        left_bar = t.Frame(left_col, bg="white", height=int(self.root.winfo_height() / 10))
        left_bar.pack(side="top", fill="x", expand="false")
        left_bar.update()
        left_bar.propagate(0)
        left_text_bar = t.Label(left_bar, bg="dark grey", text="Measurement result")
        left_text_bar.pack(side="top", fill="both", expand="true")
        left_text_bar.update()
        text_result = t.Label(left_col, bg="white", text="Show measurement results")
        text_result.pack(side="top", fill="both", expand="true")

        # begin right part of screen
        right_col = t.Frame(self.root, bg="white", width=int(self.root.winfo_width() / 2))
        right_col.pack(side="left", fill="y", expand="false")
        right_col.update()
        right_col.propagate(0)
        right_bar = t.Frame(right_col, bg="white", height=int(self.root.winfo_height() / 10))
        right_bar.pack(side="top", fill="x", expand="false")
        right_bar.update()
        right_bar.propagate(0)
        right_text_bar = t.Label(right_bar, bg="dark grey", text="Patient history")
        right_text_bar.pack(side="top", fill="both", expand="true")
        right_text_bar.update()
        text_history = t.Label(right_col, bg="white", text="Show patient result history")
        text_history.pack(side="top", fill="both", expand="true")

        # exit button for testing purposes
        exit_button = t.Button(self.root, activebackground="dark grey", activeforeground='white', bg="black",
                               fg="white", state="normal", text="Again", command=lambda: self.change_page(1))
        exit_button.update()
        exit_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)
        # end exit button

    def stop(self, *args):
        sys.exit(0)


app = App()
