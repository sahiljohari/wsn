# import matplotlib
# matplotlib.use('TkAgg')
#
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# # implement the default mpl key bindings
# from matplotlib.backend_bases import key_press_handler
#
#
# from matplotlib.figure import Figure
#
# import sys
# if sys.version_info[0] < 3:
#     import Tkinter as Tk
# else:
#     import tkinter as Tk
#
# root = Tk.Tk()
# root.wm_title("Embedding in TK")
#
#
# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = arange(0.0, 3.0, 0.01)
# s = sin(2*pi*t)
#
# a.plot(t, s)
#
#
# # a tk.DrawingArea
# canvas = FigureCanvasTkAgg(f, master=root)
# canvas.show()
# canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
#
# toolbar = NavigationToolbar2TkAgg(canvas, root)
# toolbar.update()
# canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
#
#
# def on_key_event(event):
#     print('you pressed %s' % event.key)
#     key_press_handler(event, canvas, toolbar)
#
# canvas.mpl_connect('key_press_event', on_key_event)
#
#
# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#
# button = Tk.Button(master=root, text='Quit', command=_quit)
# button.pack(side=Tk.BOTTOM)
#
# Tk.mainloop()
# # If you put root.destroy() here, it will cause an error if
# # the window is closed with the window manager.

# import matplotlib
# matplotlib.use('TkAgg')
#
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
#
# import sys
# if sys.version_info[0] < 3:
#     import Tkinter as Tk
# else:
#     import tkinter as Tk
#
#
# def destroy(e):
#     sys.exit()
#
# root = Tk.Tk()
# root.wm_title("Embedding in TK")
#
#
# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = arange(0.0, 3.0, 0.01)
# s = sin(2*pi*t)
#
# a.plot(t, s)
# a.set_title('Tk embedding')
# a.set_xlabel('X axis label')
# a.set_ylabel('Y label')
#
#
# # a tk.DrawingArea
# canvas = FigureCanvasTkAgg(f, master=root)
# canvas.show()
# canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
#
# canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
#
# button = Tk.Button(master=root, text='Quit', command=sys.exit)
# button.pack(side=Tk.BOTTOM)
#
# Tk.mainloop()

import numpy as np
import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()

fig = plt.figure(1)
# plt.ion()
t = np.arange(0.0,3.0,0.01)
s = np.sin(np.pi*t)
plt.plot(t,s)

canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()

def update():
    s = np.cos(np.pi*t)
    plt.plot(t,s)
    #d[0].set_ydata(s)
    fig.canvas.draw()

plot_widget.grid(row=0, column=0)
tk.Button(root,text="Update",command=update).grid(row=0, column=1)
root.mainloop()

#!/usr/bin/python3

# from tkinter import *
# fields = 'Nodes', 'Average Degree', 'Topology', 'Show Graph Coloring'
#
# def fetch(entries):
#    for entry in entries:
#       field = entry[0]
#       text  = entry[1].get()
#       print('%s: "%s"' % (field, text))
#
# def makeform(root, fields):
#    entries = []
#    for field in fields:
#       row = Frame(root)
#       lab = Label(row, width=15, text=field, anchor='w')
#       ent = Entry(row)
#       row.pack(side=TOP, fill=X, padx=5, pady=5)
#       lab.pack(side=LEFT)
#       ent.pack(side=RIGHT, expand=YES, fill=X)
#       entries.append((field, ent))
#    return entries
#
# if __name__ == '__main__':
#    root = Tk()
#    ents = makeform(root, fields)
#    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
#    b1 = Button(root, text='Show',
#           command=(lambda e=ents: fetch(e)))
#    b1.pack(side=LEFT, padx=5, pady=5)
#    b2 = Button(root, text='Quit', command=root.quit)
#    b2.pack(side=LEFT, padx=5, pady=5)
#    root.mainloop()