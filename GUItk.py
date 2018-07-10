import tkinter as t
import sys


class App():
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
            3: self.generate_page_three
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
        top_bar = t.Frame(self.root, bg="white", height=int(self.root.winfo_height() / 10))
        top_bar.pack(side="top", fill="x", expand="false")
        top_bar.update()
        top_bar.pack_propagate(0)
        top_text = t.Label(top_bar, bg="white", text=title)
        top_text.pack(side="top", fill="both", expand="true")
        top_text.update()
        back_button = t.Button(top_bar, activebackground="dark grey", activeforeground="white", bg="black", fg="white",
                               text="Back", command=lambda: self.change_page(1))
        back_button.pack()
        back_button.update()
        back_button.place(relheight=1, relwidth=0.15)
        instruction_bar = t.Frame(self.root, bg="grey", height=int(self.root.winfo_height() * 0.3))
        instruction_bar.pack(fill="x")
        instruction_text = t.Label(instruction_bar, bg="grey", text="Instructions for use...")
        instruction_text.place(relheight=1, relwidth=1)
        bottom_frame = t.Frame(self.root, bg="white")
        bottom_frame.pack(side="bottom", fill="both", expand="true")
        bottom_frame.update()
        bottom_frame.pack_propagate(0)
        measure_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                  fg="green", disabledforeground="red", state="disabled", text="Measure")
        measure_button.update()
        measure_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)
        precond_button = t.Button(bottom_frame, activebackground="dark grey", activeforeground="white", bg="black",
                                  fg="white", text="Pre-condition check",
                                  command=lambda: measure_button.config(state="normal"))
        precond_button.update()
        precond_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.3)


    def generate_page_three(self):
        print("nope, not yet")

    def stop(self, *args):
        sys.exit(0)


app = App()
