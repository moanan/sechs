#!/usr/bin/env python3

import tkinter as tk
import rospy
import time

from sechs_odrive.msg import *

SAVED_POINTS = []
EXECUTE = False

window = tk.Tk()
window.title("teaching")
window.geometry("350x400")

sb = tk.Scrollbar(window)    # set scrollabr
sb.pack(side="right",fill="y")  # set scrollabr diapaly
lb_teach = tk.Listbox(window, width=45, heigh=15, yscrollcommand=sb.set)
lb_teach.pack()
sb.config(command=lb_teach.yview)


def button_save_point_clicked():
    global VALUES, SAVED_POINTS
    lb_teach.insert(tk.END,"A1:%.2f  A2:%.2f  A3:%.2f  A4:%.2f  A5:%.2f  A6:%.2f" % (VALUES[0], VALUES[1], VALUES[2], VALUES[3], VALUES[4], VALUES[5]))
    SAVED_POINTS.append([VALUES[0], VALUES[1], VALUES[2], VALUES[3], VALUES[4], VALUES[5]])


def button_execute_clicked():
    global EXECUTE
    if EXECUTE:
        button_execute.config(text="execute")
    else:
        button_execute.config(text="stop")
    EXECUTE = not EXECUTE


def teach_execute():
    global PUB, SAVED_POINTS
    for i in range(len(SAVED_POINTS)):
        PUB.publish(SAVED_POINTS[i])
        time.sleep(5)


def main_loop():
    global EXECUTE, SAVED_POINTS
    if EXECUTE:
        teach_execute()
        if not loop_var.get():
            button_execute_clicked()
    window.after(1000, main_loop)


loop_var = tk.BooleanVar()
tk.Checkbutton(window, text="loop", variable=loop_var, onvalue=True, offvalue=False).pack()
tk.Button(window, text="save point", command=button_save_point_clicked).pack()
button_execute = tk.Button(window, text="execute", command=button_execute_clicked)
button_execute.pack()

main_loop()

# =================
# ROS communication
# =================

VALUES = [0.0] * 6


def callback_feedback(feedback):
    for i in range(6):
        VALUES[i] = feedback.pos.values[i]


rospy.init_node('teaching_gui', anonymous=False)
rospy.Subscriber('Sechs/Encoder_Feedback', Sechs_State, callback_feedback)
PUB = rospy.Publisher('Sechs/Position_Command', Sechs_Pos , queue_size=10)

window.mainloop()

rospy.spin()
