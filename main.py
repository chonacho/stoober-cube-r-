import opengl_test
from tkinter import *
from pygame.locals import *
import pickle

keybinds = {opengl_test.upLeft: K_w, opengl_test.leftDown: K_a, opengl_test.downRight: K_s, opengl_test.rightUp: K_d, opengl_test.frontClock: K_q, opengl_test.backClock: K_e}


def getAllChildWidgets(widget):
    children = []
    children.extend(widget.winfo_children())
    for child in children:
        children.extend(getAllChildWidgets(child))
    return children


class OpeningScreen(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.startButton = Button(self, text='Simulator', command=self.start, font=('times', 20))
        self.instructionButton = Button(self, text='Help', command=self.showInstructions, font=('times', 20))
        self.instructions = Label(self, text='Use WASDEQ controls for rotating faces and arrow keys for rotating the whole cube', font=('times', 20))
        self.returnFromInstructionsButton = Button(self, text='Click to go back', command=self.returnFromInstructions, font=('times', 12))
        self.startButton.grid(row=0)
        self.instructionButton.grid(row=1)
        for widget in getAllChildWidgets(self):
            widget.config(bg='LightSteelBlue1')
        self.config(bg='LightSteelBlue1', padx=100, pady=100)
        self.grid()

    def start(self):
        opengl_test.CubeAnimation(keybinds)

    def showInstructions(self):
        print('Use WASDEQ controls for rotating faces and arrow keys for rotating the whole cube')
        self.startButton.grid_forget()
        self.instructionButton.grid_forget()
        self.instructions.grid(row=1)
        self.returnFromInstructionsButton.grid(row=2)

    def returnFromInstructions(self):
        self.startButton.grid(row=0)
        self.instructionButton.grid(row=1)
        self.instructions.grid_forget()
        self.returnFromInstructionsButton.grid_forget()



master = Tk()
OpeningScreen(master)
master.mainloop()
