import os
import sys
import tkinter as t
from PIL import ImageTk, Image
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import RPi.GPIO as GPIO
import TESTmath as Test
import numpy as n
import threading


class App:
    # define main properties
    page = 4
    height = 600
    width = 1024
    patient_id = -1

    def __init__(self):
        self.root = t.Tk()
        self.root.config(bg="light grey")
        self.root.title("T.E.S.T.")
        self.root.pack_propagate(0)
        self.root.resizable(0, 0)
        self.root.geometry('%(a)d' % {'a': self.width} + 'x' + '%(b)d' % {'b': self.height})
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.stop)
        self.root.update()
        self.generate_objects()
        self.root.mainloop()

    def keyboardcall0(self, username_box, password_box):
        username_box.focus()

        def callback():
            os.system('florence')
            os.system('florence show')
            username_box.bind('<Tab>', lambda e: password_box.focus())
        board = threading.Thread(target=callback)
        board.start()

    def keyboardcall1(self, password_box):
        password_box.focus()

        def callback():
            os.system('florence')
            os.system('florence show')
        board = threading.Thread(target=callback)
        board.start()

    def keyboardcall2(self, patient_box):
        patient_box.focus()

        def callback():
            os.system('florence')
            os.system('florence show')
        board = threading.Thread(target=callback)
        board.start()

    def generate_objects(self, *args):
        """Function to generate pages"""
        switcher = {
            0: self.generate_login,
            1: self.generate_page_one,
            2: self.generate_page_two,
            4: self.generate_boot,
            5: self.generate_new_account,
        }
        switcher[self.page]()

    def checklist(self, measure_button):
        """Check if sample and/or hood are inserted/closed"""
        # GPIO 20 for hood, GPIO 21 for sample
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if GPIO.input(20) == 0:
            if GPIO.input(21) == 0:
                print("Cover not closed. Please close the cover.")
            else:
                print("Sample not inserted. Please insert sample.")
        else:
            measure_button.config(state="normal")

    def save_data(self, username, password):
        """Function to save newly added account data"""
        if username == '' or password == '':
            error_frame = t.Frame(self.root, bg="light grey")
            error_frame.place(relheight=0.05, relwidth=0.25, relx=0.375, rely=0.55)
            error_text = t.Label(error_frame, fg="red", bg="light grey", text="Please enter a username and password")
            error_text.pack(side="bottom", fill="both", expand="true")
        else:
            with open("./textfiles/accounts.txt", "a") as usernames:
                usernames.write(', ' + str(username))
                usernames.close()
            with open("./textfiles/passwords.txt", "a") as passwords:
                passwords.write(', ' + str(password))
                passwords.close()
            self.change_page(0)

    def save_measurements(self, measures, pre_fourier, avg, res):
        """Function to save measurements of the last measuring"""
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
        filename = "./textfiles/Measurements_Patient_" + str(self.patient_id) + ".txt"
        with open(filename, "a") as measurements:
            measurements.write("Measurements " + st + ": \n")
            for measure in measures:
                measurements.write(str(measure) + '\n')
            measurements.write("\n")
            measurements.write("Average = " + str(avg))
            measurements.write("\n\n")
            measurements.write("Result = " + str(res))
            measurements.write("\n\n\n\n")
            measurements.write("Pre-Fourier:")
            counter = 0
            for fourier in pre_fourier:
                measurements.write(str(fourier) + '\n')
                counter += 1
                if counter == 20:
                    measurements.write("\n")
                    counter = 0
            measurements.close()
        self.send_to_mail(filename)

    def send_to_mail(self, name):
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

        filename = name
        attachment = open(name, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("tuesensingteam@gmail.com", "rcr!6vkd=2u")
        text = msg.as_string()
        server.sendmail("tuesensingteam@gmail.com", "tuesensingteam@gmail.com", text)
        server.quit()

    def change_page(self, number):
        """Function to switch pages"""
        self.page = number
        for kid in self.root.winfo_children():
            kid.destroy()
        self.generate_objects()

    def admin_login(self, username, password):
        """Admin login function"""
        if username == 'admin' and password == 'admin':
            self.change_page(5)
        else:
            error_frame = t.Frame(self.root, bg="light grey")
            error_frame.place(relheight=0.05, relwidth=0.233, relx=0.4, rely=0.55)
            error_text = t.Label(error_frame, fg="red", bg="light grey", text="Admin data incorrect, access denied")
            error_text.pack(side="bottom", fill="both", expand="true")

    def login(self, username, password):
        """Login function"""
        usernames = []
        accounts = open("./textfiles/accounts.txt", "r")
        for user in list(accounts):
            user = user.split(', ')
        usernames.extend(user)
        accounts.close()

        passwords = []
        code = open("./textfiles/passwords.txt", "r")
        for word in list(code):
            word = word.split(', ')
        passwords.extend(word)
        code.close()

        if str(username) not in usernames or str(password) not in passwords:
            error_frame = t.Frame(self.root, bg="light grey")
            error_frame.place(relheight=0.05, relwidth=0.233, relx=0.4, rely=0.55)
            error_text = t.Label(error_frame, fg="red", bg="light grey", text="Username or password incorrect")
            error_text.pack(side="bottom", fill="both", expand="true")
        else:
            i = usernames.index(username)
            if password == passwords[i]:
                self.change_page(1)
            else:
                error_frame = t.Frame(self.root, bg="light grey")
                error_frame.place(relheight=0.05, relwidth=0.233, relx=0.4, rely=0.55)
                error_text = t.Label(error_frame, fg="red", bg="light grey", text="Username or password incorrect")
                error_text.pack(side="bottom", fill="both", expand="true")

    def generate_boot(self):
        back_label = t.Label(self.root, height=self.root.winfo_height(), width=self.root.winfo_width(), bg="grey")
        back_label.pack()
        img = ImageTk.PhotoImage(Image.open("./textfiles/logo.jpg"))
        main_label = t.Label(back_label, image=img)
        main_label.image = img
        main_label.pack()
        self.root.update()
        self.root.after(5000)
        self.change_page(0)

    # login screen
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
        username_box.bind('<Button-1>', lambda e: self.keyboardcall0(username_box, password_box))
        # label and box for password
        pwd_label = t.Label(entry_frame, bg="light grey", text="Password:")
        pwd_label.place(relheight=0.1, relwidth=0.4, relx=0.1, rely=0.5)
        password_box = t.Entry(entry_frame, show="*")
        password_box.place(relheight=0.1, relwidth=0.4, relx=0.5, rely=0.5)
        password_box.bind('<Button-1>', lambda e: self.keyboardcall1(password_box))
        # create login button
        login_button = t.Button(entry_frame, text="Login", bg="dark grey",
                                command=lambda: self.login(username=username_box.get(), password=password_box.get()))
        login_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.8)

        create_button = t.Button(self.root, text="Create new account", bg="dark grey",
                                 command=lambda: self.admin_login(username=username_box.get(),
                                                                  password=password_box.get()))
        create_button.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.9)
        logout_button = t.Button(self.root, text="Shutdown", bg="dark grey",
                                 command=lambda: os._exit(0))
        logout_button.place(relheight=0.1, relwidth=0.2, relx=0.8, rely=0.9)

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
                                 command=lambda: [self.save_data(username=username_box.get(),
                                                                 password=password_box.get())])
        create_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.8)

    # start page
    def generate_page_one(self):
        description = "Here will be the description of the machine..."
        bottom_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() / 2),
                               bg="light grey")
        bottom_frame.pack(side="bottom", fill="x", expand="false")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        top_text = t.Label(self.root, bg="grey", text=description)
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        entry_frame = t.Frame(bottom_frame, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg="light grey")
        entry_frame.pack(side="top", expand="false")
        entry_frame.update()
        entry_frame.propagate(0)
        patient_label = t.Label(bottom_frame, bg="light grey", text="Enter Patient ID:")
        patient_label.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.1)
        patient_box = t.Entry(entry_frame)
        patient_box.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.2)
        patient_box.bind('<Button-1>', lambda e: self.keyboardcall2(patient_box))
        bottom_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                 fg="white",
                                 text="Start", command=lambda: self.start_machine(patient_box, patient_label))
        bottom_button.update()
        bottom_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.45)

    def start_machine(self, patient, label):
        p = patient.get()
        if p != "":
            try:
                int(p)
                if int(p) < 0:
                    label.config(text="Not a Patient ID")
                    label.config(foreground="red")
                    return
                else:
                    self.patient_id = int(p)
                    self.change_page(2)
            except ValueError:
                label.config(text="Not an integer")
                label.config(foreground="red")
                return
        else:
            label.config(foreground="red")
        return

    # measure page
    def generate_page_two(self):
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
                               text="Back", command=lambda: self.change_page(1))
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        # begin upper part of screen
        output_bar = t.Frame(self.root, bg="grey", height=int(self.root.winfo_height() * 0.3))
        output_bar.pack(fill="x")
        output_bar.update()
        output_text = t.Label(output_bar, bg="grey", text="Instructions for use...")
        output_text.place(relheight=0.5, relwidth=1)
        output_text.update()
        loading_frame = t.Frame(output_bar, bg="grey")
        loading_frame.place(relheight=0.2, relwidth=0.8, relx=0.1, rely=0.5)
        loading_frame.update()
        loading_bar = t.Frame(loading_frame, bg="grey")
        loading_bar.place(relheight=0.8, relwidth=0, relx=0.01, rely=0.1)
        loading_text = t.Label(output_bar, bg="grey", text="")
        loading_text.place(relheight=0.3, relwidth=1, rely=0.7)
        # begin lower part of screen
        bottom_frame = t.Frame(self.root, bg="white")
        bottom_frame.pack(side="bottom", fill="both", expand="true")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        measure_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                  fg="green", disabledforeground="red", state="disabled", text="Measure",
                                  command=lambda: self.run(output_text, loading_frame, loading_bar, loading_text))
        measure_button.update()
        measure_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)
        # make precondition button update the properties of the measure button
        precond_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                  fg="white", text="Pre-condition check",
                                  command=lambda: self.checklist(measure_button))
        precond_button.update()
        precond_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.3)
        logout_button = t.Button(self.root, text="Logout and shutdown", bg="dark grey",
                                 command=lambda: os._exit(0))
        logout_button.place(relheight=0.1, relwidth=0.2, relx=0.8, rely=0.9)

        redo = t.Button(self.root, text="Measure again", bg="dark grey",
                        command=lambda: self.change_page(1))
        redo.place(relheight=0.1, relwidth=0.2, relx=0.2, rely=0.9)

    def stop(self, *args):
        sys.exit(0)

    # ========== HERE FOLLOW THE MAIN FUNCTIONS ==========

    def getAmp(self):
        """Input: none
           Output: single amplitude of +- 10Hz freq as measured."""
        tt, adc_values = Test.get_values()
        x, y = Test.fourierten(tt, adc_values)
        return y, adc_values

    def getResult(self, avg):
        """Input: single amplitude
           Output: single result value"""
        return n.abs(2 * (avg * avg) - 30 * avg + 20)
        # TODO

    def convert(self, adc_values):
        voltage = []
        for entry in adc_values:
            value = (5/32678) * entry
            voltage.append(value)
        return voltage

    def run(self, output_text, loading_frame, loading_bar, loading_text):
        """Input: none
           Output: none"""
        loading_frame.config(bg="black")
        loading_frame.update()
        loading_bar.config(bg="light grey")
        loading_bar.place(relwidth=0)
        loading_bar.update()
        loading_text.config(text="Do actuation...")
        loading_text.update()

        measurements = []
        pre_fourier = []
        # Test.actuation()
        progress = 0

        for z in range(20):
            progress = progress + 0.04

            loading_bar.place(relwidth=progress)
            loading_bar.update()
            loading_text.config(text="Get Measurement " + str(z))
            loading_text.update()

            y, adc_values = self.getAmp()
            voltage = self.convert(adc_values)
            measurements.append(y)
            pre_fourier.append(voltage)
            time.sleep(10)
            if z == 10:
                Test.actuation()

        loading_bar.place(relwidth=0.88)
        loading_bar.update()
        loading_text.config(text="Save Results...")
        loading_text.update()

        avg = sum(measurements) / len(measurements)
        res = self.getResult(avg)
        output_text.config(text="Average = " + str(avg) + "\n" + "Result = " + str(res))
        self.save_measurements(measurements, pre_fourier, avg, res)

        loading_bar.place(relwidth=0.98)
        loading_bar.update()
        loading_text.config(text="Done")
        loading_text.update()


app = App()
