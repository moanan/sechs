#!/usr/bin/env python3

import tkinter as tk
import rospy
import time

from sechs_odrive.msg import Sechs_Axes


def value_adjust():
    global labels_value, VALUS
    if control_mode_var.get() == 0:
        for i in range(6):
            labels_value[i].config(text=("%.3f" % VALUS[i]))
    else:
        # **************************
        # to be developed
        # **************************
        pass


def button_plus_clicked(index):
    global PUB, VALUS_SET
    VALUS_SET.values[index] += control_speed_var.get()
    PUB.publish(VALUS_SET)


def button_minus_clicked(index):
    global PUB, VALUS_SET
    VALUS_SET.values[index] -= control_speed_var.get()
    PUB.publish(VALUS_SET)


def function_config():
    global labels_control
     # Axes
    if control_mode_var.get() == 0:
        for i in range(6):
            labels_control[i].config(text=("A%d"%(i+1)))
    else:
        labels_control[0].config(text="X")
        labels_control[1].config(text="Y")
        labels_control[2].config(text="Z")
        labels_control[3].config(text="A")
        labels_control[4].config(text="B")
        labels_control[5].config(text="C")


window = tk.Tk()
window.title("sechs")
window.geometry("400x300")

# ===============
# function_select
# ===============

function_select_f = tk.Frame(window)
function_select_f.pack()

control_mode_var = tk.IntVar()
function1_rb = tk.Radiobutton(function_select_f, text='Axes', font=12, variable=control_mode_var, value=0, command=function_config)
function1_rb.pack(side="left")
function2_rb = tk.Radiobutton(function_select_f, text='Cartesian Base', font=12, variable=control_mode_var, value=1, command=function_config)
function2_rb.pack(side="left")
function3_rb = tk.Radiobutton(function_select_f, text='Cartesian TCF', font=12, variable=control_mode_var, value=2, command=function_config)
function3_rb.pack(side="left")

# ===============
# speed select
# ===============

function_select_s = tk.Frame(window)
function_select_s.pack()

control_speed_var = tk.DoubleVar()
speed1_rb = tk.Radiobutton(function_select_s, text='slow', font=12, variable=control_speed_var, value=0.005)
speed1_rb.pack(side="left")
speed2_rb = tk.Radiobutton(function_select_s, text='medium', font=12, variable=control_speed_var, value=0.015)
speed2_rb.pack(side="left")
speed3_rb = tk.Radiobutton(function_select_s, text='fast', font=12, variable=control_speed_var, value=0.025)
speed3_rb.pack(side="left")

# ================
# 6 inputs outputs
# ================

control_panel_f = tk.Frame(window)
control_panel_f.pack()


def add_control_panel(index):
    control_panel_temp = tk.Frame(control_panel_f)
    control_panel_temp.pack()

    label_control = tk.Label(control_panel_temp, text=("A%d" % (index+1)), width=8, height=1, bg="white", font=12)
    label_control.pack(side="left", padx=10)
    label_value = tk.Label(control_panel_temp, text="0.0", width=8, height=1, bg="white", font=12)
    label_value.pack(side="left", padx=10)

    tk.Button(control_panel_temp, text="+", command=lambda: button_plus_clicked(index)).pack(side="left")
    tk.Button(control_panel_temp, text="-", command=lambda: button_minus_clicked(index)).pack(side="left")

    return label_control, label_value


labels_control, labels_value = [], []
for i in range(6):
    lc, lv = add_control_panel(i)
    labels_control.append(lc)
    labels_value.append(lv)

# =================
# ROS communication
# =================

VALUS = [0.0] * 6
VALUS_SET = Sechs_Axes()


def callback_encoder_feedback(sechs_axes):
    for i in range(6):
        VALUS[i] = sechs_axes.values[i]
    value_adjust()

flag_continue = False
rospy.init_node('gui', anonymous=False)
# time.sleep(5)
rospy.Subscriber('Sechs/Encoder_Feedback', Sechs_Axes, callback_encoder_feedback)
PUB = rospy.Publisher('Sechs/Position_Command', Sechs_Axes , queue_size=10)

window.mainloop()

rospy.spin()
