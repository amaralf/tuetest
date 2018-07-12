import tkinter as t
import sys


class App():
    # define main properties
    page = 1
    height = 600
    width = 1024

    def __init__(self):
        self.root = t.Tk()
        self.root.pack_propagate(0)
        self.root.resizable(0, 0)
        self.root.geometry('%(a)d' % {'a': self.width} + 'x' + '%(b)d' % {'b': self.height})
        self.root.bind('<Escape>', self.stop)
        self.root.update()
        self.generate_objects()
        self.root.mainloop()

    def generate_objects(self, *args):
        switcher = {
            1: self.generate_page_one,
            2: self.generate_page_two,
            3: self.generate_page_three,
            4: self.generate_page_four
        }
        switcher[self.page]()

    def change_page(self, number):
        self.page = number
        for kid in self.root.winfo_children():
            kid.destroy()
        self.generate_objects()

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
                                 text="Measure", command=lambda: self.change_page(2))
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
                               fg="white", state="normal", text="Exit", command=lambda: sys.exit(0))
        exit_button.update()
        exit_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)
        # end exit button

    def stop(self, *args):
        sys.exit(0)


app = App()
