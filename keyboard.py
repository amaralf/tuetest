# import modules
try:
    import Tkinter
except:
    import tkinter as Tkinter

import pyautogui

__author__ = '''

######################################################
                By S.S.B Group                          
######################################################

    Suraj Singh
    Admin
    S.S.B Group
    surajsinghbisht054@gmail.com
    http://bitforestinfo.blogspot.com/

    Note: We Feel Proud To Be Indian
######################################################
'''

# ========== Configurations ====================
BUTTON_BACKGROUND = "black"
MAIN_FRAME_BACKGROUND = "dark grey"
BUTTON_LOOK = "ridge"  # flat, groove, raised, ridge, solid, or sunken
TOP_BAR_TITLE = "Python Virtual KeyBoard."
TOPBAR_BACKGROUND = "skyblue"
TRANSPARENCY = 0.7
FONT_COLOR = "white"
FONT = "Calibri"

# ==============================================
keys = [
    [
        # =========================================
        # ===== Keyboard Configurations ===========
        # =========================================
        [
            ("Character_Keys"),
            ({'side': 'top', 'expand': 'yes', 'fill': 'both'}),
            [
                ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'backspace'),
                ('Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '_'),
                ('-', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', "Enter"),
                ("Space", 'z', 'x', 'c', 'v', 'b', 'n', 'm', '(', ')', ',', "Shift")
            ]
        ]
    ]
]


# Create key event
def create_keyboard_event(numlock, capslock, controller, key):
    return


# Frame Class
class Keyboard(Tkinter.Frame):
    def __init__(self, *args, **kwargs):
        Tkinter.Frame.__init__(self, *args, **kwargs)

        # Function For Creating Buttons
        self.create_frames_and_buttons()

    # Function For Extracting Data From KeyBoard Table
    # and then provide us a well looking
    # keyboard gui
    def create_frames_and_buttons(self):
        # take section one by one
        for key_section in keys:
            # create Separate Frame For Every Section
            store_section = Tkinter.Frame(self)
            store_section.pack(side='left', expand='yes', fill='both', padx=10, pady=10, ipadx=10, ipady=10)

            for layer_name, layer_properties, layer_keys in key_section:
                store_layer = Tkinter.LabelFrame(store_section)  # , text=layer_name)
                # store_layer.pack(side='top',expand='yes',fill='both')
                store_layer.pack(layer_properties)
                for key_bunch in layer_keys:
                    store_key_frame = Tkinter.Frame(store_layer)
                    store_key_frame.pack(side='top', expand='yes', fill='both')
                    for k in key_bunch:
                        k = k.capitalize()
                        if len(k) <= 3:
                            store_button = Tkinter.Button(store_key_frame, text=k, width=2, height=2, font=(FONT, 16))
                        else:
                            store_button = Tkinter.Button(store_key_frame, text=k.center(5, ' '), height=2, font=(FONT, 16))
                        if " " in k:
                            store_button['state'] = 'disable'

                        store_button['relief'] = BUTTON_LOOK
                        store_button['bg'] = BUTTON_BACKGROUND
                        store_button['fg'] = FONT_COLOR

                        store_button['command'] = lambda q=k.lower(): self.button_command(q)
                        store_button.pack(side='left', fill='both', expand='yes')
        return

    # Function For Detecting Pressed Keyword.
    def button_command(self, event):
        if event != "shift":
            pyautogui.press(event)
            pyautogui.keyUp("shift")
        else:
            pyautogui.keyDown("shift")
        return


class top_moving_mechanism:
    def __init__(self, root, label):
        self.root = root
        self.label = label

    def motion_activate(self, kwargs):
        w, h = (self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        (x, y) = (kwargs.x_root, kwargs.y_root)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        return


# Creating Main Window
def main(root):
    k = Keyboard(root, bg=MAIN_FRAME_BACKGROUND)

    # Configuration
    # root.overrideredirect(True)
    # root.wait_visibility(root)
    # root.wm_attributes('-alpha', TRANSPARENCY)
    # Custom
    # f = Tkinter.Frame(root)
    # t_bar = Tkinter.Label(f, text=TOP_BAR_TITLE, bg=TOPBAR_BACKGROUND)
    # t_bar.pack(side='left', expand="yes", fill="both")
    # mechanism = top_moving_mechanism(root, t_bar)
    # t_bar.bind("<B1-Motion>", mechanism.motion_activate)
    # Tkinter.Button(f, text="[X]", command=root.destroy).pack(side='right')
    # f.pack(side='top', expand='yes', fill='both')
    k.place(relheight=0.5, relwidth=1.0, relx=0.0, rely=0.5)
    # root.mainloop()
    return


# Function Trigger
if __name__ == '__main__':
    main()
