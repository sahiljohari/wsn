from tkinter import *
import tkinter.messagebox as msg

class GUI:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.drawButton = Button(frame, text='Plot', command=self.plotGraph)
        self.drawButton.pack(side=LEFT)

        self.quitButton = Button(frame, text='Quit', command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def plotGraph(self):
        print('And it gets plotted')

def dummy():
    print('Doing nothing')

root = Tk()
# gui = GUI(root)
# Message Box
msg.showinfo('Message', 'Fuck you!')
def wannaquit():
    response = msg.askquestion('Q1', 'Do you fuck?')

    if response == 'yes':
        root.quit()

# Menu
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='New', command=dummy)
subMenu.add_command(label='Configure', command=dummy)
subMenu.add_separator()
subMenu.add_command(label='Quit', command=wannaquit)

animMenu = Menu(menu)
menu.add_cascade(label='Edit', menu=animMenu)
animMenu.add_command(label='Draw nodes', command=dummy)
animMenu.add_command(label='Draw Edges', command=dummy)
animMenu.add_separator()
animMenu.add_command(label='Clear', command=wannaquit)

# Toolbar
toolbar = Frame(root, bg = 'yellow')
insertButtons = Button(toolbar, text='Plot', command=dummy)
insertButtons.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

# Status Bar
status = Label(root, text='Do nothing', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)



root.mainloop()
