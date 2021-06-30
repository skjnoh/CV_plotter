# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter as tk
from tkinter import Entry

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg
from Equations import *
import numpy
from scipy.optimize import curve_fit
from EChemAnalysis import *
import csv



# Things to fix/add
# 1. Tk window popping up and staying when loading file

# Usage:
# 1. Run CVtoList until all CVs are loaded to CVList.
# 2. Use plotCVlist to make a plot of all loaded CVs
class App(tk.Tk):

    def __init__(self, CVList):
        super().__init__()
        self.filename = ''
        self.delimiter = tk.StringVar()
        self.delimiter.set('\t')

        self.CVfileSource = tk.IntVar()
        self.CVfileSource.set(101)

        CVsources = [("AutoLab", 101),
                     ("DigiElch", 102)]


        self.LoadFileBtn = tk.Button(self, text = 'Load CV File',
                             command = self.fileprompt)
        self.LoadFileBtn.pack(padx=120, pady=30)

        self.filenamebox = tk.Label(self)
        self.filenamebox.pack()

        self.Fc_pot_entry = tk.Entry(self) # note that this is string and will have to be converted later.
        self.Fc_pot_entry.insert(0, 0.000)
        self.Fc_pot_entry.pack()

        #tk.Radiobutton(self, text = 'tab', variable=self.delimiter, value='\t').pack()
        #tk.Radiobutton(self, text=';', variable=self.delimiter, value=';').pack()

        for program, val in CVsources:
            tk.Radiobutton(self, text = program, variable=self.CVfileSource, value=val).pack()
        #self.delimiter_entry = tk.Entry(self)
        #self.delimiter_entry.insert(0,string=";")
        #self.delimiter_entry.pack()

        #self.debugBtn = tk.Button(self, text = 'debug', command = self.checkvar)
        #self.debugBtn.pack()

        self.plotCV = tk.Button(self, text = 'Plot CVs', command = self.PlotCV_app)
        self.plotCV.pack()

        #make space for matplotlib objects
        self.fig = matplotlib.figure.Figure(figsize=(6, 4.5),dpi=100)

        self.plot = self.fig.add_subplot(111)
        self.plot.set_ylabel("Current (A)")
        self.plot.set_xlabel("Potential (V vs Fc/Fc$^+$)")

        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        self.toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(self.canvas,self)
        self.toolbar.update()

        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()


    def checkvar(self): # for debugging
        print(type(self.Fc_pot_entry.get()))

    def fileprompt(self):
        self.filename = tk.filedialog.askopenfilename()
        if self.filename:
            with open(app.filename) as rawdata:
                self.delimiter.set(csv.Sniffer().sniff(rawdata.read(10000)).delimiter)
            self.filenamebox.config(text="File: "+self.filename)
            CVtoList(CVList, self.filename, float(self.Fc_pot_entry.get()), self.delimiter.get(), self.CVfileSource.get())


    def PlotCV_app(self):
        plotCVlist(CVList, self.plot)
        #self.plot.set_ylabel("Current (A)")
        #self.plot.clear()
        self.fig.tight_layout()
        self.canvas.draw()

#method for loading CV into a dictionary. (Asks for file and then appends it to Dict)
def CVtoList(CVList, filename, Fc_pot = 0, delimiter = ";", CVfileSource = 101):
    f = open(filename, "r", encoding='utf-8-sig')
    if CVfileSource == 102:
        CVList.append(pd.read_csv(f, names = ['WE(1).Potential (V)','WE(1).Current (A)'],delimiter=delimiter,skiprows=2, engine='python'))
        CVList[-1]['WE(1).Current (A)'] = -CVList[-1]['WE(1).Current (A)']


    if CVfileSource == 101:
        CVList.append(pd.read_csv(f, delimiter=delimiter, engine='python'))
        if Fc_pot != 0:
            if "Potential applied (V)" in CVList[-1].columns:
                CVcopy = CVList[-1]["Potential applied (V)"].rename("Potential vs Fc/Fc+ (V)") - Fc_pot
            else:
                CVcopy = CVList[-1]["WE(1).Potential (V)"].rename("Potential vs Fc/Fc+ (V)") - Fc_pot
            CVList[-1] = pd.concat((CVList[-1], CVcopy), axis=1)

    f.close()

def plotCVlist(CVList, ax):
    for CV in CVList:
        try:
            CV.plot('Potential vs Fc/Fc+ (V)', y='WE(1).Current (A)',ax=ax)
        except:
            CV.plot('WE(1).Potential (V)', y='WE(1).Current (A)', ax=ax) #should be potential applied instead
            #plt.xlabel("Potential vs pseudoref (V)")
        ax.set_xlabel("Potential vs Fc/Fc$^+$ (V)")
        ax.set_ylabel("Current (A)")


def getECSA(CVList):
    Cap_array = ECSA_Analysis(CVList[-1])
    popt, pcov = curve_fit(linear, Cap_array[0], Cap_array[1])
    print("slope = " + str(popt))
    return popt, Cap_array

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    CVList = []
    app = App(CVList)
    app.title('title!')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
