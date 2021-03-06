# Software developed and tested exclusively and exquisitely for T.E.S.T. 2018
# By T.T.P. Franken and R.P.W. Schmidt.

"""These are all the packages/imports that we use to run our software
   Note that TESTmath is the other Python file. We imported that one here, so that we can call
   the functions from that file here as well"""
import os
import sys
import socket
import tkinter as t
import re
from PIL import ImageTk, Image
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decimal import Decimal
import RPi.GPIO as GPIO
import TESTmath as Test
import numpy as n
import keyboard as keyboard


class App:
    """Here we declare the entire app/GUI. Everything our program does is written inside the App class.
       We also declare the main properties of our program here, like the colors and font type/size."""
    page = 4  # 4 is boot
    height = 600
    width = 1024
    patient_id = -1
    font = "Calibri"
    color1 = "#71b5cc"  # sea blue
    color2 = "#add8e6"  # baby blue
    color3 = "white"
    color4 = "dark blue"
    normalfontsize = 14
    biggerfontsize = 18

    def __init__(self):
        """Here we declare all attributes that are initialized at startup. Think about the background color, the program
           title or a specific keybind to shut down the program."""
        self.root = t.Tk()
        self.root.config(bg=self.color2)
        self.root.title("T.E.S.T.")
        self.root.pack_propagate(0)
        self.root.resizable(0, 0)
        self.root.geometry('%(a)d' % {'a': self.width} + 'x' + '%(b)d' % {'b': self.height})
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        self.root.bind('<Escape>', self.stop)
        self.root.update()
        self.generate_objects()
        self.root.mainloop()

    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = str(s.getsockname()[0])
            return ip
        except socket.error:
            return "IP cannot be found"


    def generate_objects(self, *args):
        """Function to generate pages."""
        switcher = {
            0: self.generate_login,
            1: self.generate_page_patientID,
            2: self.generate_page_measure,
            3: self.generate_page_results,
            4: self.generate_boot,
            5: self.generate_new_account,
            6: self.generate_settings,
        }
        switcher[self.page]()

    def change_page(self, number):
        """Function to switch pages"""
        self.page = number
        for kid in self.root.winfo_children():
            kid.destroy()
        self.generate_objects()

    def checklist(self, output_text, loading_frame, loading_bar, loading_text,
                  button_list, mail_button):
        """Check if sample and/or hood are inserted/closed and display an error message when appropriate."""
        # GPIO 20 for hood, GPIO 21 for sample
        GPIO.setmode(GPIO.BCM)
        # GPIO.PUD_DOWN is an attribute that declares the pin == 0 even if nothing is connected, so it would normally be
        # 'floating' between 0 and 1. This is fixed by that attribute.
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if GPIO.input(20) == 0:
            if GPIO.input(21) == 0:
                output_text.config(text="Please close the lid.")
                output_text.config(fg="red")
                output_text.update()
            else:
                output_text.config(text="Please insert sample.")
                output_text.config(fg="red")
                output_text.update()
            return
        else:
            output_text.config(text="Preconditions satisfied. Measuring...")
            output_text.config(fg="black")
            output_text.update()
            for button in button_list:
                # print(button)
                button.config(state="disabled")
                button.update()
            mail_button.config(state="disabled")
            mail_button.update()
            self.run(output_text, loading_frame, loading_bar, loading_text, button_list, mail_button)

    def save_data(self, username, password):
        """Function to save newly added account data."""
        if username == '' or password == '':
            error_text = t.Label(self.root, fg="red", bg=self.color2, text="Please enter a username and password")
            error_text.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.4)
        else:
            with open("/home/pi/Desktop/tuetest/textfiles/accounts.txt", "a") as usernames:
                usernames.write(', ' + str(username))
                usernames.close()
            with open("/home/pi/Desktop/tuetest/textfiles/passwords.txt", "a") as passwords:
                passwords.write(', ' + str(password))
                passwords.close()
            self.change_page(0)

    def save_results(self, res, mgLres):
        """Function to save the new results with a timestamp."""
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
        filename = "/home/pi/Desktop/tuetest/textfiles/Results_Patient_" + str(self.patient_id) + ".txt"
        dirname = os.path.dirname(filename)
        # print(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, "a") as rez:
            rez.write("TimeStamp: " + str(st) + "\n")
            rez.write("Concentration in uM: " + str(res) + "\n")
            rez.write("Concentration in mg/L: " + str(mgLres)+"\n\n")

    def save_measurements(self, measures, avgs, devs, res, mgLres, meds):
        """Function to save measurements of the last measuring attempt."""
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
        filename = "/home/pi/Desktop/tuetest/textfiles/Measurements_Patient_" + str(self.patient_id) + ".txt"
        dirname = os.path.dirname(filename)
        # print(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, "a") as measurements:
            measurements.write("Measurements " + st + ": \n")
            for measure in measures:
                measurements.write(str(measure) + ' ')
            measurements.write("\n\n Averages: ")
            for avg in avgs:
                measurements.write(str(avg)+" ")
            measurements.write("\n\n Standard Deviations: ")
            for dev in devs:
                measurements.write(str(dev) + " ")
            measurements.write("\n\n Medians: ")
            for med in meds:
                measurements.write(str(med) + " ")
            measurements.write("\n\n")
            measurements.write("Concentration in pM: " + str(res) + "\n")
            measurements.write("Concentration in mg/L: " + str(mgLres) + "\n\n\n\n")
            measurements.close()

    def send_to_mail(self, name, prettyname):
        """Function to email the results of the current patient to ourselves."""
        fromaddr = "tuesensingteam@gmail.com"
        toaddr = "tuesensingteam@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
        msg['Subject'] = "T.E.S.T " + str(st) + " results"
        body = "Results are enclosed."
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(name, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % prettyname)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("tuesensingteam@gmail.com", "rcr!6vkd=2u")
        text = msg.as_string()
        server.sendmail("tuesensingteam@gmail.com", "tuesensingteam@gmail.com", text)
        server.quit()

    def admin_login(self, username, password):
        """Admin login function to create a new account. Displays an error message if not correct."""
        if username == 'admin' and password == 'admin':
            self.change_page(5)
        else:
            error_text = t.Label(self.root, fg="red", bg=self.color2, text="Admin data incorrect, access denied")
            error_text.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.4)

    def login(self, username, password):
        """Login function. Displays an error message if the user and/or password do not match or do not (yet) exist."""
        usernames = []
        accounts = open("/home/pi/Desktop/tuetest/textfiles/accounts.txt", "r")
        # accounts = open("/home/pi/Desktop/tuetest/textfiles/accounts.txt", "r")
        for user in list(accounts):
            user = user.split(', ')
        usernames.extend(user)
        accounts.close()

        passwords = []
        code = open("/home/pi/Desktop/tuetest/textfiles/passwords.txt", "r")
        # code = open("/home/pi/Desktop/tuetest/textfiles/passwords.txt", "r")
        for word in list(code):
            word = word.split(', ')
        passwords.extend(word)
        code.close()

        if str(username) not in usernames or str(password) not in passwords:
            error_text = t.Label(self.root, fg="red", bg=self.color2, text="Username or password incorrect")
            error_text.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.4)
        else:
            i = usernames.index(username)
            if password == passwords[i]:
                self.change_page(1)
            else:
                error_text = t.Label(self.root, fg="red", bg=self.color2, text="Username or password incorrect")
                error_text.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.4)

    def generate_boot(self):
        """This is the splash screen you will see when you run our program. This will be visible for 5 seconds
           before continuing to the next page."""
        back_label = t.Label(self.root, height=self.root.winfo_height(), width=self.root.winfo_width(), bg="grey")
        back_label.pack()
        img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/tuetest/textfiles/logo.jpg"))
        main_label = t.Label(back_label, image=img)
        main_label.image = img
        main_label.pack()
        self.root.update()
        self.root.after(5000)
        self.change_page(0)

    def generate_login(self):
        """This is the login page. Here, the user can login with any existing and matching credentials."""
        # create upper frame with text
        title_bar = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() / 10),
                            bg=self.color3)
        title_bar.pack(side="top", fill="x", expand="false")
        title_bar.update()
        title_bar.propagate(0)
        self.includelogo(title_bar)
        ipaddr = self.get_ip_address()
        ipholder = t.Label(title_bar, bg=self.color3, fg=self.color4, text=ipaddr)
        ipholder.place(relwidth=0.15, relheight=1.0, relx=0)
        description_label = t.Label(title_bar, bg=self.color3, text="A Biosensor for measuring Vancomycin",
                                    font=(self.font, self.normalfontsize), fg=self.color4)
        description_label.place(relwidth=0.4, relheight=1.0, relx=0.3)
        description_label.update()
        login_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.3),
                              bg=self.color3)
        login_frame.pack(side="top", fill="x", expand="false")
        login_frame.update()
        login_frame.propagate(0)

        # create entry box
        entry_frame = t.Frame(login_frame, width=int(self.root.winfo_width()),
                              height=int(self.root.winfo_height() / 2), bg=self.color2)
        entry_frame.pack(side="top", expand="false")
        entry_frame.update()
        entry_frame.propagate(0)

        # label and box for username
        user_label = t.Label(entry_frame, bg=self.color2, text="Username:", font=(self.font, self.normalfontsize))
        user_label.place(relheight=0.3, relwidth=0.1, relx=0.3, rely=0.05)
        username_box = t.Entry(entry_frame, font=(self.font, self.normalfontsize), bg=self.color3)
        username_box.place(relheight=0.3, relwidth=0.2, relx=0.4, rely=0.05)
        username_box.bind('<Button-1>', lambda e: username_box.focus())

        # label and box for password
        pwd_label = t.Label(entry_frame, bg=self.color2, text="Password:", font=(self.font, self.normalfontsize))
        pwd_label.place(relheight=0.3, relwidth=0.1, relx=0.3, rely=0.35)
        password_box = t.Entry(entry_frame, show="*", font=(self.font, self.normalfontsize), bg=self.color3)
        password_box.place(relheight=0.3, relwidth=0.2, relx=0.4, rely=0.35)
        password_box.bind('<Button-1>', lambda e: password_box.focus())

        # create login button
        login_button = t.Button(entry_frame, text="Login", bg=self.color4, fg=self.color3,
                                font=(self.font, self.normalfontsize),
                                activebackground=self.color2, activeforeground=self.color3,
                                command=lambda: self.login(username=username_box.get(), password=password_box.get()))
        login_button.place(relheight=0.3, relwidth=0.2, relx=0.40, rely=0.7)

        # button to create a new account
        create_button = t.Button(self.root, text="Create new account", bg=self.color4, fg=self.color3,
                                 font=(self.font, self.normalfontsize),
                                 activebackground=self.color2, activeforeground=self.color3,
                                 command=lambda: self.admin_login(username=username_box.get(),
                                                                  password=password_box.get()))

        # button to shutdown the sensor or shutdown the program if admin credentials and entered first
        create_button.place(relheight=0.1, relwidth=0.2, relx=0.0, rely=0.4)
        logout_button = t.Button(self.root, text="Shutdown", bg=self.color4, fg=self.color3,
                                 activebackground=self.color2, activeforeground=self.color3,
                                 font=(self.font, self.normalfontsize), command=lambda: self.logout(username_box.get(),
                                                                                                    password_box.get()))
        logout_button.place(relheight=0.1, relwidth=0.2, relx=0.8, rely=0.4)

        # add keyboard to the screen
        keyboard.main(self.root)

    def logout(self, usr, pwd):
        """This function determines to shutdown the sensor or just close the program depending on the credentials."""
        if usr == "admin" and pwd == "admin":
            os._exit(0)
        else:
            os.system("sudo poweroff")
        return

    def includelogo(self, parent_label):
        """Like the name implies, this function shows the T.E.S.T. logo at the top right of the screen."""
        img = Image.open("/home/pi/Desktop/tuetest/textfiles/LogoSmall.png")
        # img = Image.open("/home/pi/Desktop/tuetest/textfiles/LogoSmall.png")

        logo_label = t.Label(parent_label)
        logo_label.place(relx=0.9, relwidth=0.1, relheight=1.0)
        logo_label.update()
        img = img.resize((logo_label.winfo_width(), logo_label.winfo_height()))
        picture = ImageTk.PhotoImage(img)
        logo_label.config(image=picture)
        logo_label.image = picture
        logo_label.update()

    def generate_new_account(self):
        """Function to generate a new account. This page can only be accessed by logging in as admin. The newly created
           account will then immediately be added and can be used from that moment on."""
        title_bar = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.1),
                            bg=self.color3)
        title_bar.pack(side="top", fill="x", expand="false")
        title_bar.update()
        title_bar.propagate(0)
        description_label = t.Label(title_bar, bg=self.color3, text="A Biosensor for measuring Vancomycin",
                                    font=(self.font, self.normalfontsize), fg=self.color4)
        description_label.place(relwidth=0.4, relheight=1.0, relx=0.3)
        description_label.update()
        self.includelogo(title_bar)

        # create upper frame with text
        account_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.3),
                                bg=self.color3)
        account_frame.pack(side="top", fill="x", expand="false")
        account_frame.update()
        account_frame.propagate(0)

        # create entry box
        input_frame = t.Frame(account_frame, width=int(self.root.winfo_width()),
                              height=int(self.root.winfo_height() / 2), bg=self.color2)
        input_frame.pack(side="top", expand="false")
        input_frame.update()
        input_frame.propagate(0)

        # label and box for username
        user_label = t.Label(input_frame, bg=self.color2, text="Username:", font=(self.font, self.normalfontsize))
        user_label.place(relheight=0.3, relwidth=0.1, relx=0.3, rely=0.05)
        username_box = t.Entry(input_frame, font=(self.font, self.normalfontsize), bg=self.color3)
        username_box.place(relheight=0.3, relwidth=0.2, relx=0.4, rely=0.05)

        # label and box for password
        pwd_label = t.Label(input_frame, bg=self.color2, text="Password:", font=(self.font, self.normalfontsize))
        pwd_label.place(relheight=0.3, relwidth=0.1, relx=0.3, rely=0.35)
        password_box = t.Entry(input_frame, show="*", font=(self.font, 24), bg=self.color3)
        password_box.place(relheight=0.3, relwidth=0.2, relx=0.4, rely=0.35)

        # create login button
        create_button = t.Button(input_frame, text="Create", bg=self.color4, font=(self.font, self.normalfontsize),
                                 activebackground=self.color2, activeforeground=self.color3,
                                 command=lambda: [self.save_data(username=username_box.get(),
                                                                 password=password_box.get())],
                                 fg=self.color3)
        create_button.place(relheight=0.3, relwidth=0.2, relx=0.4, rely=0.7)
        keyboard.main(self.root)

    def generate_page_patientID(self):
        """This function created the page where the user fills in the ID of the patient. This can be anything, from
           just a string of text to numbers, or a combination of both."""
        title = "Patient ID"
        top_bar = t.Frame(self.root, bg=self.color3, height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)

        # begin text and button of top bar
        top_text = t.Label(top_bar, bg=self.color3, text=title, fg=self.color4, font=(self.font, 36))
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                               fg=self.color3, text="\u21A9" + " Back", font=(self.font, self.normalfontsize),
                               command=lambda: self.change_page(0))
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        self.includelogo(top_bar)

        # create top frame
        top_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.4),
                            bg=self.color2)
        top_frame.pack(side="top", fill="x", expand="false")
        top_frame.update()
        top_frame.pack_propagate(0)

        # create entry frame for the patientID with a label
        entry_frame = t.Frame(top_frame, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg=self.color2)
        entry_frame.pack(side="top", expand="false")
        entry_frame.update()
        entry_frame.propagate(0)
        patient_label = t.Label(top_frame, bg=self.color2, fg=self.color4, text="Enter Patient ID:",
                                font=(self.font, self.normalfontsize))
        patient_label.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.1)
        patient_box = t.Entry(entry_frame, bg=self.color3, font=(self.font, self.normalfontsize))
        patient_box.place(relheight=0.2, relwidth=0.5, relx=0.25, rely=0.3)
        patient_box.bind('<Button-1>', lambda e: patient_box.focus())
        bottom_button = t.Button(top_frame, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                                 fg=self.color3, font=(self.font, self.normalfontsize),
                                 text="Start", command=lambda: self.start_machine(patient_box, patient_label))
        bottom_button.update()
        bottom_button.place(relheight=0.2, relwidth=0.3, relx=0.35, rely=0.6)

        # add keyboard
        keyboard.main(self.root)

    def start_machine(self, patient, label):
        """This function checks if the user actually entered a PatientID."""
        p = patient.get()
        if p != "":
            self.patient_id = p
            self.change_page(2)
            return
        else:
            label.config(text="Please enter a Patient ID")
            label.config(foreground="red")
        return

    def generate_page_measure(self):
        """Function to generate the measure page. Here, you can start a measurement."""
        filename = "/home/pi/Desktop/tuetest/textfiles/Measurements_Patient_" + str(self.patient_id) + ".txt"
        prettyname = "Measurements_Patient_" + str(self.patient_id) + ".txt"
        title = "Measurement"
        # begin top bar of screen
        top_bar = t.Frame(self.root, bg=self.color3, height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)

        # begin text and button of top bar
        top_text = t.Label(top_bar, bg=self.color3, fg=self.color4, text=title, font=(self.font, 36))
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                               fg=self.color3, text="\u21A9" + " Back", font=(self.font, self.normalfontsize),
                               command=lambda: self.change_page(1), disabledforeground="red")
        back_button.pack()
        back_button.update()
        button_list = [back_button]
        back_button.place(relheight=1, relwidth=0.15)
        self.includelogo(top_bar)

        # begin upper part of screen
        output_bar = t.Frame(self.root, bg=self.color2, height=int(self.root.winfo_height() * 0.6))
        output_bar.pack(fill="x")
        output_bar.update()
        output_text = t.Label(output_bar, bg=self.color2,
                              text="Click the 'Measure' button.\n" +
                                   "It will check whether the sensor is ready to measure.\n"
                                   "If so, it will initiate the measurement.",
                              font=(self.font, self.normalfontsize))
        output_text.place(relheight=0.6, relwidth=1)
        output_text.update()
        loading_frame = t.Frame(output_bar, bg=self.color2)
        loading_frame.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.6)
        loading_frame.update()
        loading_bar = t.Frame(loading_frame, bg=self.color2)
        loading_bar.place(relheight=0.8, relwidth=0, relx=0.01, rely=0.1)
        loading_text = t.Label(output_bar, bg=self.color2, text="", font=(self.font, self.normalfontsize))
        loading_text.place(relheight=0.2, relwidth=1, rely=0.7)

        # begin lower part of screen
        bottom_frame = t.Frame(self.root, bg=self.color2)
        bottom_frame.pack(side="bottom", fill="both", expand="true")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        measure_button = t.Button(bottom_frame, activebackground=self.color2, activeforeground=self.color3,
                                  bg=self.color4,
                                  fg=self.color3, text="Measure", font=(self.font, self.normalfontsize),
                                  disabledforeground="red",
                                  command=lambda: self.checklist(output_text, loading_frame, loading_bar, loading_text,
                                                                 button_list, mail_button))
        measure_button.update()
        measure_button.place(relheight=0.4, relwidth=0.2, relx=0.2, rely=0.0)
        button_list.append(measure_button)
        actuation_button = t.Button(bottom_frame, activebackground=self.color2, activeforeground=self.color3,
                                  bg=self.color4,
                                  fg=self.color3, text="Settings", font=(self.font, self.normalfontsize),
                                  disabledforeground="red",
                                  command=lambda: self.change_page(6))
        actuation_button.update()
        actuation_button.place(relheight=0.4, relwidth=0.2, relx=0.6, rely=0.0)
        button_list.append(actuation_button)
        logout_button = t.Button(self.root, text="Logout and shutdown", bg=self.color4, font=(self.font,
                                                                                              self.normalfontsize),
                                 activeforeground=self.color3, activebackground=self.color2,
                                 fg=self.color3, disabledforeground="red", command=lambda: os.system("sudo poweroff"))
        logout_button.place(relheight=0.1, relwidth=0.3, relx=0.675, rely=0.85)
        button_list.append(logout_button)
        mail_button = t.Button(self.root, text="Mail", bg=self.color4, font=(self.font,
                                                                             self.normalfontsize),
                               activeforeground=self.color3, activebackground=self.color2,
                               fg=self.color3, disabledforeground="red",
                               command=lambda: self.send_to_mail(filename, prettyname))
        mail_button.place(relheight=0.1, relwidth=0.3, relx=0.35, rely=0.85)
        try:
            open(filename, "r")
        except FileNotFoundError:
            mail_button.config(state="disabled")
        else:
            mail_button.config(state="normal")
        results_button = t.Button(self.root, text="Results", bg=self.color4,
                                  font=(self.font, self.normalfontsize),
                                  activeforeground=self.color3, activebackground=self.color2, fg=self.color3,
                                  disabledforeground="red",
                                  command=lambda: self.change_page(3))
        results_button.place(relheight=0.1, relwidth=0.3, relx=0.025, rely=0.85)
        button_list.append(results_button)

    def generate_page_results(self):
        """Function to generate a page that shows all measurement results for the current patient."""
        title = "Results of Patient " + str(self.patient_id)

        # begin top bar of screen
        top_bar = t.Frame(self.root, bg=self.color3, height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)

        # begin text and button of top bar
        top_text = t.Label(top_bar, bg=self.color3, fg=self.color4, text=title, font=(self.font, 36))
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                               fg=self.color3, text="\u21A9" + " Back", font=(self.font, self.normalfontsize),
                               command=lambda: self.change_page(2), disabledforeground="red")
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        self.includelogo(top_bar)

        # begin upper part of screen
        fileframe = t.Frame(self.root, bg=self.color3)
        fileframe.place(relheight=0.9, relwidth=1.0, relx=0.0, rely=0.1)
        filename = "/home/pi/Desktop/tuetest/textfiles/Results_Patient_" + str(self.patient_id) + ".txt"
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            filetext = "There are no results yet for patient " + str(self.patient_id) + "."
        else:
            filetext = file.read()
        filelabel = t.Text(fileframe, bg=self.color2, font=(self.font, self.biggerfontsize))
        filelabel.insert("end", filetext)
        filelabel.place(relheight=1, relwidth=0.9, relx=0, rely=0)
        filescroll = t.Scrollbar(fileframe, command=filelabel.yview)
        filelabel.config(yscrollcommand=filescroll.set)
        filelabel.config(state="disabled")
        filescroll.place(relheight=1, relwidth=0.1, relx=0.9, rely=0)
        fileframe.update()
        filelabel.update()
        filescroll.update()

    def generate_settings(self):
        """Function to generate a page that shows all measurement results for the current patient."""
        title = "Settings"
        # begin top bar of screen
        top_bar = t.Frame(self.root, bg=self.color3, height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)

        # begin text and button of top bar
        top_text = t.Label(top_bar, bg=self.color3, fg=self.color4, text=title, font=(self.font, 36))
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                               fg=self.color3, text="\u21A9" + " Back", font=(self.font, self.normalfontsize),
                               command=lambda: self.saveandquit(filename, filelabel, error), disabledforeground="red")
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        self.includelogo(top_bar)

        # begin upper part of screen
        fileframe = t.Frame(self.root, bg=self.color3)
        fileframe.place(relheight=0.4, relwidth=0.3, relx=0.0, rely=0.1)
        filename = "/home/pi/Desktop/tuetest/textfiles/Settings.txt"
        try:
            file = open(filename, "r+")
        except FileNotFoundError:
            open(filename, "w+")
            file = open(filename, "r+")
        filetext = file.read()
        filelabel = t.Text(fileframe, bg="white", font=(self.font, self.biggerfontsize))
        filelabel.insert("end", filetext)
        filelabel.place(relheight=1, relwidth=0.9, relx=0, rely=0)
        filescroll = t.Scrollbar(fileframe, command=filelabel.yview)
        filelabel.config(yscrollcommand=filescroll.set)
        filescroll.place(relheight=1, relwidth=0.1, relx=0.9, rely=0)
        fileframe.update()
        filelabel.update()
        filescroll.update()
        explanation_frame = t.Frame(self.root, bg=self.color3)
        explanation_frame.place(relheight=0.4, relwidth=0.7, relx=0.3, rely=0.1)
        explanation_frame.update()
        text = "This is the settings page. On this page, you can configure the measurement rounds and the" \
               " actuations.\n\n"
        text += "To add a measurement round, add 'measure(amount of pulses, amount of seconds between)'" \
                " on a new line. One pulse measurement takes 0.2 seconds.\n\n"
        text += "To add an actuation round, add 'actuate(amount of actuations, amount of seconds between," \
                " amount of time after)' on a new line."
        explanation = t.Label(explanation_frame, wraplength=explanation_frame.winfo_width()-20, bg=self.color2,
                              text=text, font=(self.font, self.normalfontsize), justify='left')
        explanation.place(relx = 0.0, rely = 0.0, relheight=0.8, relwidth=1.0)
        explanation.update()
        error = t.Label(explanation_frame, fg='red', wraplength=explanation_frame.winfo_width()-20, bg=self.color2,
                              font=(self.font, self.normalfontsize), justify='left')
        error.place(relx=0.0, rely=0.8, relheight=0.2, relwidth=1.0)
        keyboard.main(self.root)

    def saveandquit(self, filename, filelabel, error):
        file = open(filename, "w")
        text = filelabel.get("1.0", 'end')
        text = text.rstrip()
        lines = text.splitlines()
        if len(lines) == 0:
            error.config(text="You must have input.")
            return
        for line in lines:
            regex = re.compile(r'-?\w+')
            single = regex.findall(line)
            if len(single) == 0:
                error.config(text="Remove the last newline.")
                return
            command = single[0]
            if command == 'measure':
                if len(single) < 3:
                    error.config(text="You forgot one of the function arguments")
                    return
                if len(single) >= 4:
                    error.config(text="One command per line")
                    return
                amount = int(single[1])
                seconds = int(single[2])
                if amount < 0:
                    error.config(text="Negative amount specified.")
                    return
                if seconds < 0:
                    error.config(text="Negative time specified.")
                    return
            elif command == 'actuate':
                if len(single) < 4:
                    error.config(text="You forgot one of the function arguments")
                    return
                if len(single) >= 5:
                    error.config(text="One command per line")
                    return
                amount = int(single[1])
                seconds = int(single[2])
                endseconds = int(single[3])
                if amount < 0:
                    error.config(text="Negative amount specified.")
                    return
                if seconds < 0 or endseconds < 0:
                    error.config(text="Negative time specified.")
                    return
                if not isinstance(single[1], int) or not isinstance(single[2], int) or not isinstance(single[3], int):
                    error.config(text="Check your numbers for other types (decimal numbers or strings, for example).")
            else:
                error.config(text="Unknown command used. Please remove or change it.")
                return
        file.write(text)
        self.change_page(2)

    def stop(self, *args):
        """"Function that shuts down the program when <Escape> is pressed."""
        sys.exit(0)

    # ========== HERE FOLLOW THE MAIN FUNCTIONS ==========

    def getAmp(self):
        """Input: none
           Output: single amplitude of +- 10Hz freq as measured."""
        tt, adc_values = Test.get_values()
        voltage = self.convert(adc_values)
        x, y = Test.fourierten(tt, voltage)
        return y, voltage, tt

    def calibration_curve(self, median):
        """Input: avg
           Output: Concentration"""
        ans = -2e9*n.log(median/0.0096)       # ans is in pM unit
        uM_ans = round(ans/1e6, 3)                  # ans is in uM unit
        mgLans = ans*1e-9*1449.25*0.97546           # mgLans is in mg/L unit
        return ans, uM_ans, mgLans

    def getResult(self, meassets):
        """Input: single amplitude
           Output: single result value"""
        avgs = []
        devs = []
        meds = []
        for set in meassets:
            # print(set)
            med = Test.outliercombat(set)
            avg = sum(set)/len(set)
            predev = 0
            for number in set:
                k = n.square(number - avg)
                predev = predev + k
            divisible = (len(set) - 1)
            if divisible == 0:
                dev = -1
            else:
                middev = predev / (len(set) - 1)
                dev = n.sqrt(middev)
            avgs.append(avg)
            devs.append(dev)
            meds.append(med)
        # target = avgs[(len(avgs)-1)]
        target = meds[0]
        ans, res, mgLres = self.calibration_curve(target)
        return ans, res, mgLres, devs, avgs, target, meds

    def convert(self, adc_values):
        """Function to convert the bitstring readout to Volts."""
        voltage = []
        for entry in adc_values:
            value = (5 / 32678) * int(entry)
            voltage.append(value)
        return voltage

    def run(self, output_text, loading_frame, loading_bar, loading_text, button_list, mail_button):
        """Main function for the actual measurement. This function controls the DAC's and the ADC.
           Input: none
           Output: none"""
        filename = "/home/pi/Desktop/tuetest/textfiles/Measurements_Patient_" + str(self.patient_id) + ".txt"
        settingsname = "/home/pi/Desktop/tuetest/textfiles/Settings.txt"
        output_text.config(text="Measuring patient "+str(self.patient_id)+"...")
        output_text.config(fg="black")
        output_text.update()
        loading_frame.config(bg=self.color4)
        loading_frame.update()
        loading_bar.config(bg=self.color2)
        loading_bar.place(relwidth=0)
        loading_bar.update()

        measurements = []
        progress = 0

        settings = open(settingsname, 'r')
        text = settings.read()
        lines = text.splitlines()
        pieceprogress = 0.9 / len(lines)
        measureamounts = []
        action = 0
        actions = len(lines)
        for line in lines:
            action += 1
            regex = re.compile(r'-?\w+')
            sep = regex.findall(line)
            if sep[0] == 'measure':
                amount = int(sep[1])
                seconds = int(sep[2])
                piece = pieceprogress/amount
                measureamounts.append(amount)
                returnvalues, progress = self.measure(amount, seconds, piece, loading_bar, loading_text, progress, action, actions)
                measurements.append(returnvalues)
            if sep[0] == 'actuate':
                amount = int(sep[1])
                seconds = int(sep[2])
                endseconds = int(sep[3])
                piece = pieceprogress/float(sep[1])
                progress = self.actuate(amount, seconds, endseconds, piece, loading_bar, loading_text, progress, action, actions)

        loading_bar.place(relwidth=0.90)
        loading_bar.update()
        loading_text.config(text="Saving Results...")
        loading_text.update()
        ans, uMres, mgLres, devs, avgs, peaksignal, meds = self.getResult(measurements)
        roundmgLres = round(mgLres, 3)
        textstring = "Measurement of patient " + str(self.patient_id) + " finished.\n\n"
        # textstring += "\n The original signal intensity is " + str(roundsignal) + "\n"
        textstring += "The resulting concentration of Vancomycin is " + str(uMres) + " uM \n or " + \
                      str(roundmgLres) + " mg/L.\n" + "A2f peak is "+ str(peaksignal) + ".\n"
        if mgLres < 2.0 or mgLres > 110:
            textstring += "Vancomycin concentration might be near zero."
        # textstring += "\n\n Press the Measure Button to measure again."
        output_text.config(text=textstring, font='bold')
        self.save_measurements(measurements, avgs, devs, uMres, mgLres, meds)
        self.save_results(uMres, roundmgLres)
        loading_bar.place(relwidth=0.98)
        loading_bar.update()
        loading_text.config(text="Finished")
        loading_text.update()
        for button in button_list:
            button.config(state="normal")
            button.update()
        try:
            open(filename, "r")
        except FileNotFoundError:
            mail_button.config(state="disabled")
        else:
            mail_button.config(state="normal")

    def measure(self, amount, waittime, piece, loading_bar, loading_text, progress, action, actions):
        returnvalues = []
        for z in range(amount):

            loading_text.config(text="Action " + str(action) + " of " + str(actions) + ":\n" +
                                     "Get Measurement " + str(z + 1) + " of " + str(amount))
            loading_text.update()

            y, voltage, tt = self.getAmp()
            returnvalues.append(y)
            if z != amount-1:
                time.sleep(waittime)
            progress = progress + piece
            loading_bar.place(relwidth=progress)
            loading_bar.update()
        return returnvalues, progress

    def actuate(self, amount, waittime, endtime, piece, loading_bar, loading_text, progress, action, actions):
        for z in range(amount):
            loading_text.config(text="Action " + str(action) + " of " + str(actions) + ":\n" +
                                     "Do Actuation " + str(z + 1) + " of " + str(amount))
            loading_text.update()
            Test.actuation()
            if z < amount-1:
                time.sleep(waittime)
            if z == amount-1:
                time.sleep(endtime)
            progress += piece
            loading_bar.place(relwidth=progress)
            loading_bar.update()
        return progress


app = App()
