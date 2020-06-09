#!/usr/bin/env python3

from tkinter import *

import rospy


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master


root = Tk()
app = Window(root)
root.mainloop()

