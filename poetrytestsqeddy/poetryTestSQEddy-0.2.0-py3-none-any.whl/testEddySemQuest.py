"""
This is a simple test program.
I am going to use it to try and utilize Poetry and its tools.

Edward Ferrara Jr.
SemQuest Inc.
"""

import matplotlib.pyplot as plt
from tkinter import *

class Application:

    def __init__(self, master):
        self.master = master
        master.title("Test GUI")

        #create lists to store points
        self.xPts = []
        self.yPts = []

        #Create input prompts and buttons
        self.xInputLabel = Label(master, text="Enter x\n coordinate:")
        self.yInputLabel = Label(master, text="Enter y\n coordinate:")
        self.xInput = Entry(master, width=10)
        self.yInput = Entry(master, width=10)

        self.enterButton = Button(master, text="Add to points", command=self.addToPts)
        self.graphButton = Button(master, text="Graph!", command=self.graphToPlot)
        self.quitButton = Button(master, text="Quit", command=self.quitApplication)
        self.clearPtsButton = Button(master, text="Clear points", command=self.clearPts)

        #Organize layout of buttons and labels
        self.xInputLabel.grid(row=0, column=0)
        self.yInputLabel.grid(row=0, column=2)
        self.xInput.grid(row=0, column=1)
        self.yInput.grid(row=0, column=3)
        self.enterButton.grid(row=1, column=0, columnspan=4)
        self.graphButton.grid(row=2, column=1, columnspan=1)
        self.quitButton.grid(row=3, column=0, columnspan=4)
        self.clearPtsButton.grid(row=2, column=2, columnspan=1)

    def quitApplication(self):
        #quits application
        self.master.destroy()

    def clearPts(self):
        #clears lists of points
        self.xPts = []
        self.yPts = []

    def addToPts(self):

        #check to see if user inputted numbers into x and y boxes
        if not self.xInput.get() and not self.yInput.get():
            xyError = Label(self.master, text="Please enter a valid x and y point!")
            xyError.grid(row=3, column=0, columnspan=4)
            xyError.after(1000, xyError.grid_forget)
            return

        if not self.yInput.get():
            yError = Label(self.master, text="Please enter a valid y point!")
            yError.grid(row=4, column=0, columnspan=4)
            yError.after(1000, yError.grid_forget)
            return

        if not self.xInput.get():
            xError = Label(self.master, text="Please enter a valid x point!")
            xError.grid(row=4, column=0, columnspan=4)
            xError.after(1000, xError.grid_forget)
            return

        #add input into the x and y point lists
        self.xPts.append(int(self.xInput.get()))
        self.yPts.append(int(self.yInput.get()))

        #Clear the input field after entering them into the list
        self.xInput.delete(0, END)
        self.yInput.delete(0, END)

        #Notify user the points were successfully added
        addPtsNotif = Label(self.master, text="Added to list of points!")
        addPtsNotif.grid(row=4, column=0, columnspan=4)
        addPtsNotif.after(1000, addPtsNotif.grid_forget)

    def graphToPlot(self):

        #Check to see if there are points to graph
        if not self.xPts or not self.yPts:
            graphError = Label(self.master, text="There are no points to graph!")
            graphError.grid(row=5, column=0, columnspan=4)
            graphError.after(1000, graphError.grid_forget)
            return

        #Create max variables to know what size to make the plot
        xMax = 0
        yMax = 0

        #Go through each list in order to find max point
        for i in self.xPts:
            if i > xMax:
                xMax = i

        for y in self.yPts:
            if y > yMax:
                yMax = y

        #plot the points as a scatter plot using red circles
        plt.plot(self.xPts, self.yPts, 'ro')
        plt.axis([0, (xMax + 5), 0, (yMax + 5)])
        plt.show()

#run the gui
root = Tk()
app = Application(root)
root.mainloop()
