import opengl_test
from tkinter import *
from pygame.locals import *
import pickle

keybinds = [(K_w, opengl_test.upLeft), (K_a, opengl_test.leftUp), (K_s, opengl_test.downLeft), (K_d, opengl_test.rightUp)]


def getAllChildWidgets(widget):
    children = []
    children.extend(widget.winfo_children())
    for child in children:
        children.extend(getAllChildWidgets(child))
    return children


class OpeningScreen(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.startButton = Button(self, text='Click to open cube animation', command=self.start, font=('times', 20))
        self.instructionButton = Button(self, text='Click to show instructions', command=self.showInstructions, font=('times', 20))
        self.instructions = Label(self, text='Use WASD controls for rotating faces and arrow keys for rotating the whole cube', font=('times', 20))
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
        print('Use WASD controls for rotating faces and arrow keys for rotating the whole cube')
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
mainloop()
