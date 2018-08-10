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
import keyboard as keyboard

# Software developed and tested exclusively and exquisitely for T.E.S.T. 2018
# by T.T.P. Franken and R.P.W. Schmidt.


class App:
    # define main properties
    page = 1  # 4 is boot
    height = 600
    width = 1024
    patient_id = -1
    font = "Calibri"
    # color1 = "#d50471" # dark pink
    # color2 = "#1e4faa" # light blue
    # color3 = "#d5c5cb" # light pink
    # color4 = "#1e2c75" # dark blue
    color1 = "steel blue"
    color2 = "light blue"
    color3 = "white"
    color4 = "dark blue"
    normalfontsize = 14
    biggerfontsize = 18

    def __init__(self):
        self.root = t.Tk()
        self.root.config(bg=self.color2)
        self.root.title("T.E.S.T.")
        self.root.pack_propagate(0)
        self.root.resizable(0, 0)
        self.root.geometry('%(a)d' % {'a': self.width} + 'x' + '%(b)d' % {'b': self.height})
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.stop)
        self.root.update()
        self.generate_objects()
        self.root.mainloop()

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

    def checklist(self, output_text, loading_frame, loading_bar, loading_text,
                  back_button, logout_button, measure_button):
        """Check if sample and/or hood are inserted/closed"""
        # GPIO 20 for hood, GPIO 21 for sample
        GPIO.setmode(GPIO.BCM)
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
            back_button.config(state="disabled")
            logout_button.config(state="disabled")
            measure_button.config(state="disabled")
            back_button.update()
            logout_button.update()
            measure_button.update()
            self.run(output_text, loading_frame, loading_bar, loading_text, back_button, logout_button, measure_button)

    def save_data(self, username, password):
        """Function to save newly added account data"""
        if username == '' or password == '':
            error_text = t.Label(self.root, fg="red", bg=self.color2, text="Please enter a username and password")
            error_text.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.4)
        else:
            with open("/home/pi/Desktop/tuetest/textfiles/accounts.txt", "a") as usernames:
                usernames.write(', ' + str(username))
                usernames.close()
            with open("/home/pi/Desktop/tuetest/textfiles/passwords.txt", "a") as passwords:
                passwords.write(', ' + str(password))
                passwords.close()
            self.change_page(0)

    def save_measurements(self, measures, avg1, avg2, dev1, dev2):
        """Function to save measurements of the last measuring"""
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
        filename = "/home/pi/Desktop/tuetest/textfiles/Measurements_Patient_" + str(self.patient_id) + ".txt"
        dirname = os.path.dirname(filename)
        print(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, "a") as measurements:
            measurements.write("Measurements " + st + ": \n")
            for measure in measures:
                measurements.write(str(measure) + ' ')
            measurements.write("\n")
            measurements.write("Average first 10 = " + str(avg1))
            measurements.write("\n")
            measurements.write("Standard Deviation first 10 = " + str(dev1))
            measurements.write("\n")
            measurements.write("Average second 10 = " + str(avg2))
            measurements.write("\n")
            measurements.write("Standard Deviation second 10 = " + str(dev2))
            measurements.write("\n\n")
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
            error_text = t.Label(self.root, fg="red", bg=self.color2, text="Admin data incorrect, access denied")
            error_text.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.4)

    def login(self, username, password):
        """Login function"""
        usernames = []
        accounts = open("home/pi/Desktop/tuetest/textfiles/accounts.txt", "r")
        for user in list(accounts):
            user = user.split(', ')
        usernames.extend(user)
        accounts.close()

        passwords = []
        code = open("home/pi/Desktop/tuetest/textfiles/passwords.txt", "r")
        for word in list(code):
            word = word.split(', ')
        passwords.extend(word)
        code.close()

        if str(username) not in usernames or str(password) not in passwords:
            error_text = t.Label(self.root, fg="red", bg=self.color2, text="Username or password incorrect")
            error_text.place(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.4)
        else:
            i = usernames.index(username)
            if password == passwords[i]:
                self.change_page(1)
            else:
                error_text = t.Label(self.root, fg="red", bg=self.color2, text="Username or password incorrect")
                error_text.pack(relheight=0.1, relwidth=0.2, relx=0.4, rely=0.4)

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
        title_bar = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height()/10))
        title_bar.pack(side="top", fill="x", expand="false")
        title_bar.update()
        title_bar.propagate(0)
        title_label = t.Label(title_bar, bg=self.color2, text="T.E.S.T. 2018", font=(self.font, 32), fg=self.color3)
        title_label.pack(side="top", fill="both", expand="true")
        self.includelogo(title_label)
        description_label = t.Label(title_bar, bg=self.color2, text="A Biosensor for measuring Vancomycin",
                                    font=(self.font, self.normalfontsize), wraplength=300, fg=self.color3)
        description_label.place(relwidth=0.3, relheight=1.0)
        description_label.update()
        login_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.3),
                              bg=self.color3)
        login_frame.pack(side="top", fill="x", expand="false")
        login_frame.update()
        login_frame.propagate(0)
        # create entry box
        entry_frame = t.Frame(login_frame, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg=self.color1)
        entry_frame.pack(side="top", expand="false")
        entry_frame.update()
        entry_frame.propagate(0)
        # label and box for username
        user_label = t.Label(entry_frame, bg=self.color1, text="Username:", font=(self.font, self.normalfontsize))
        user_label.place(relheight=0.3, relwidth=0.3, relx=0.1, rely=0.05)
        username_box = t.Entry(entry_frame, font=(self.font, self.normalfontsize), bg=self.color3)
        username_box.place(relheight=0.3, relwidth=0.5, relx=0.4, rely=0.05)
        username_box.bind('<Button-1>', lambda e: username_box.focus())
        # label and box for password
        pwd_label = t.Label(entry_frame, bg=self.color1, text="Password:", font=(self.font, self.normalfontsize))
        pwd_label.place(relheight=0.3, relwidth=0.3, relx=0.1, rely=0.35)
        password_box = t.Entry(entry_frame, show="*", font=(self.font, self.normalfontsize), bg=self.color3)
        password_box.place(relheight=0.3, relwidth=0.5, relx=0.4, rely=0.35)
        password_box.bind('<Button-1>', lambda e: password_box.focus())
        # create login button
        login_button = t.Button(entry_frame, text="Login", bg=self.color4, fg=self.color3,
                                font=(self.font, self.normalfontsize),
                                activebackground=self.color2, activeforeground=self.color3,
                                command=lambda: self.login(username=username_box.get(), password=password_box.get()))
        login_button.place(relheight=0.3, relwidth=0.4, relx=0.3, rely=0.7)

        create_button = t.Button(self.root, text="Create new account", bg=self.color4, fg=self.color3,
                                 font=(self.font, self.normalfontsize),
                                 activebackground=self.color2, activeforeground=self.color3,
                                 command=lambda: self.admin_login(username=username_box.get(),
                                                                  password=password_box.get()))
        create_button.place(relheight=0.1, relwidth=0.2, relx=0.0, rely=0.4)
        logout_button = t.Button(self.root, text="Shutdown", bg=self.color4, fg=self.color3,
                                 activebackground=self.color2, activeforeground=self.color3,
                                 font=(self.font, self.normalfontsize), command=lambda: self.logout(username_box.get(),
                                                                                                    password_box.get()))
        logout_button.place(relheight=0.1, relwidth=0.2, relx=0.8, rely=0.4)
        keyboard.main(self.root)

    def logout(self, usr, pwd):
        if usr == "admin" and pwd == "admin":
            os._exit(0)
        else:
            os.system("sudo poweroff")
        return


    def includelogo(self, parent_label):
        img = Image.open("/home/pi/Desktop/tuetest/textfiles/LogoSmall.png")
        logo_label = t.Label(parent_label)
        logo_label.place(relx=0.9, relwidth=0.1, relheight=1.0)
        logo_label.update()
        img = img.resize((logo_label.winfo_width(), logo_label.winfo_height()))
        picture = ImageTk.PhotoImage(img)
        logo_label.config(image=picture)
        logo_label.image = picture
        logo_label.update()

    def generate_new_account(self):
        title_bar = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.1))
        title_bar.pack(side="top", fill="x", expand="false")
        title_bar.update()
        title_bar.propagate(0)
        title_label = t.Label(title_bar, bg=self.color2, text="T.E.S.T. 2018", font=(self.font, 36))
        title_label.pack(side="top", fill="both", expand="true")
        description_label = t.Label(title_bar, bg=self.color2, text="A Biosensor for measuring Vancomycin",
                                    font=(self.font, self.normalfontsize), wraplength=300, fg=self.color3)
        description_label.place(relwidth=0.3, relheight=1.0)
        description_label.update()
        self.includelogo(title_label)
        # create upper frame with text
        account_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() * 0.3),
                                bg=self.color3)
        account_frame.pack(side="top", fill="x", expand="false")
        account_frame.update()
        account_frame.propagate(0)
        # create entry box
        input_frame = t.Frame(account_frame, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg=self.color1)
        input_frame.pack(side="top", expand="false")
        input_frame.update()
        input_frame.propagate(0)
        # label and box for username
        user_label = t.Label(input_frame, bg=self.color1, text="Username:", font=(self.font, self.normalfontsize))
        user_label.place(relheight=0.3, relwidth=0.3, relx=0.1, rely=0.05)
        username_box = t.Entry(input_frame, font=(self.font, self.normalfontsize), bg=self.color3)
        username_box.place(relheight=0.3, relwidth=0.5, relx=0.4, rely=0.05)
        # label and box for password
        pwd_label = t.Label(input_frame, bg=self.color1, text="Password:", font=(self.font, self.normalfontsize))
        pwd_label.place(relheight=0.3, relwidth=0.3, relx=0.1, rely=0.35)
        password_box = t.Entry(input_frame, show="*", font=(self.font, 24), bg=self.color3)
        password_box.place(relheight=0.3, relwidth=0.5, relx=0.4, rely=0.35)
        # create login button
        create_button = t.Button(input_frame, text="Create", bg=self.color4, font=(self.font, self.normalfontsize),
                                 activebackground=self.color2, activeforeground=self.color3,
                                 command=lambda: [self.save_data(username=username_box.get(),
                                                                 password=password_box.get())],
                                 fg=self.color3)
        create_button.place(relheight=0.3, relwidth=0.4, relx=0.3, rely=0.7)
        keyboard.main(self.root)

    # start page
    def generate_page_one(self):
        title="Patient ID"
        top_bar = t.Frame(self.root, bg=self.color3, height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)
        # begin text and button of top bar
        top_text = t.Label(top_bar, bg=self.color3, text=title, font=(self.font, 36))
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                               fg=self.color3, text="\u21A9" + " Back", font=(self.font, self.normalfontsize),
                               command=lambda: self.change_page(0))
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        self.includelogo(top_bar)
        top_frame = t.Frame(self.root, width=self.root.winfo_width(), height=int(self.root.winfo_height() *0.4),
                               bg=self.color2)
        top_frame.pack(side="top", fill="x", expand="false")
        top_frame.update()
        top_frame.pack_propagate(0)

        entry_frame = t.Frame(top_frame, width=int(self.root.winfo_width() / 3),
                              height=int(self.root.winfo_height() / 2), bg=self.color2)
        entry_frame.pack(side="top", expand="false")
        entry_frame.update()
        entry_frame.propagate(0)
        patient_label = t.Label(top_frame, bg=self.color2, fg=self.color3, text="Enter Patient ID:",
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
        keyboard.main(self.root)

    def start_machine(self, patient, label):
        p = patient.get()
        if p != "":
            self.patient_id = p
            self.change_page(2)
            return
        else:
            label.config(text="Please enter a Patient ID")
            label.config(foreground="red")
        return

    # measure page
    def generate_page_two(self):
        title = "Measurement"
        # begin top bar of screen
        top_bar = t.Frame(self.root, bg=self.color3, height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)
        # begin text and button of top bar
        top_text = t.Label(top_bar, bg=self.color3, text=title, font=(self.font, 36))
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                               fg=self.color3, text="\u21A9" + " Back", font=(self.font, self.normalfontsize),
                               command=lambda: self.change_page(1), disabledforeground="red")
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        self.includelogo(top_bar)
        # begin upper part of screen
        output_bar = t.Frame(self.root, bg=self.color1, height=int(self.root.winfo_height() * 0.3))
        output_bar.pack(fill="x")
        output_bar.update()
        output_text = t.Label(output_bar, bg=self.color1,
                              text="Click the 'Measure' button.\n" +
                                   "It will check whether the sensor is ready to measure.\n"
                                   "If so, it will initiate the measurement.",
                              font=(self.font, self.normalfontsize))
        output_text.place(relheight=0.5, relwidth=1)
        output_text.update()
        loading_frame = t.Frame(output_bar, bg=self.color1)
        loading_frame.place(relheight=0.2, relwidth=0.8, relx=0.1, rely=0.5)
        loading_frame.update()
        loading_bar = t.Frame(loading_frame, bg=self.color1)
        loading_bar.place(relheight=0.8, relwidth=0, relx=0.01, rely=0.1)
        loading_text = t.Label(output_bar, bg=self.color1, text="")
        loading_text.place(relheight=0.3, relwidth=1, rely=0.7)
        # begin lower part of screen
        bottom_frame = t.Frame(self.root, bg=self.color3)
        bottom_frame.pack(side="bottom", fill="both", expand="true")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        measure_button = t.Button(bottom_frame, activebackground=self.color2, activeforeground=self.color3, bg=self.color4,
                                  fg=self.color3, text="Measure", font=(self.font, self.normalfontsize),
                                  disabledforeground="red",
                                  command=lambda: self.checklist(output_text, loading_frame, loading_bar, loading_text,
                                                                 back_button, logout_button, measure_button))
        measure_button.update()
        measure_button.place(relheight=0.2, relwidth=0.4, relx=0.3, rely=0.3)
        logout_button = t.Button(self.root, text="Logout and shutdown", bg=self.color4, font=(self.font, self.normalfontsize),
                                 activeforeground=self.color3, activebackground=self.color2, fg=self.color3,
                                 disabledforeground="red",
                                 command=lambda: os.system("sudo poweroff"))
        logout_button.place(relheight=0.1, relwidth=0.4, relx=0.6, rely=0.9)

    def stop(self, *args):
        sys.exit(0)

    # ========== HERE FOLLOW THE MAIN FUNCTIONS ==========

    def getAmp(self):
        """Input: none
           Output: single amplitude of +- 10Hz freq as measured."""
        tt, adc_values = Test.get_values()
        voltage = self.convert(adc_values)
        x, y = Test.fourierten(tt, voltage)
        return y, voltage, tt

    def getResult(self, meas1, meas2, halflength):
        """Input: single amplitude
           Output: single result value"""
        avg1 = sum(meas1) / halflength
        avg2 = sum(meas2) / halflength
        predev1= 0
        for number in meas1:
            k = n.square(number - avg1)
            predev1 = predev1 + k
        middev1 = predev1 / (len(meas1)-1)
        print(middev1)
        dev1 = n.sqrt(middev1)
        predev2 = 0
        for number in meas2:
            k = n.square(number - avg2)
            predev2 = predev2 + k
        middev2 = predev2 / (len(meas2)-1)
        print(middev2)
        dev2 = n.sqrt(middev2)
        return dev1, dev2, avg1, avg2

    def convert(self, adc_values):
        voltage = []
        for entry in adc_values:
            value = (5/32678) * int(entry)
            voltage.append(value)
        return voltage

    def run(self, output_text, loading_frame, loading_bar, loading_text, back_button, logout_button, measure_button):
        """Input: none
           Output: none"""
        output_text.config(text="Measuring...")
        output_text.config(fg="black")
        output_text.update()
        loading_frame.config(bg=self.color4)
        loading_frame.update()
        loading_bar.config(bg=self.color2)
        loading_bar.place(relwidth=0)
        loading_bar.update()
        loading_text.config(text="Do actuation...")
        loading_text.update()

        measurements = []
        pre_fourier = []
        times = []
        progress = 0

        for z in range(20):
            progress = progress + 0.04

            loading_bar.place(relwidth=progress)
            loading_bar.update()
            loading_text.config(text="Get Measurement " + str(z+1))
            loading_text.update()

            y, voltage, tt = self.getAmp()
            measurements.append(y)
            pre_fourier.append(voltage)
            times.append(tt)
            time.sleep(10)
            if z == 9:
                loading_text.config(text="Actuating...")
                loading_text.update()
                progress += 0.08
                loading_bar.place(relwidth=progress)
                loading_bar.update()
                Test.actuation()

        loading_bar.place(relwidth=0.93)
        loading_bar.update()
        loading_text.config(text="Saving Results...")
        loading_text.update()
        if len(measurements) != 20:
            print("more than 20 measurements")
        halflength = int(len(measurements)/2)
        meas1 = measurements[:halflength]
        print(measurements)
        print("\n")
        print(meas1)
        print("\n")
        print(len(meas1))
        meas2 = measurements[halflength:]
        print("\n")
        print(meas2)
        print("\n")
        print(len(meas2))
        # print(str(halflength) + " should be 10")
        dev1, dev2, avg1, avg2 = self.getResult(meas1, meas2, halflength)
        print("avg of first ten: " + str(avg1))
        print("avg of second ten: " + str(avg2))
        output_text.config(text="Measurement finished. Press the Measure Button to measure again.")
        self.save_measurements(measurements, avg1, avg2, dev1, dev2)
        loading_bar.place(relwidth=0.98)
        loading_bar.update()
        loading_text.config(text="Finished")
        loading_text.update()
        back_button.config(state="normal")
        logout_button.config(state="normal")
        measure_button.config(state="normal")
        back_button.update()
        logout_button.update()
        measure_button.update()


app = App()
