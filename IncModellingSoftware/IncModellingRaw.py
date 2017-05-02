"""
================================================================================
INCLINOMETER PLOTTING
================================================================================
Plot data from a borehole inclinometer as a contour graph. Data is provided as
CSV files, formatted as shown in "How To" sister document. Plots are output to
the same directory, if not specified elsewhere as PNG files. See the example
data set for the expected layout of CSV input.

Additional packages required:
tkinter
matplotlib
numpy

https://github.com/brythonick/clino-contour
"""

from tkinter import *
from tkinter import filedialog
from csv import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import numpy as np
from datetime import datetime
from os import listdir, chdir
from os.path import isfile, join, dirname, abspath
from argparse import ArgumentParser

# ============================================================================ #
# GUI STARTUP
# ============================================================================ #

class window(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        Frame.pack(self)


# ============================================================================ #
# FUNCTIONS
# ============================================================================ #

    #Browse CSV File Function
        def browse():
            csvFile = filedialog.askopenfilename(**self.browse_opt)
            csvEntry.delete(0, END)
            csvEntry.insert(0, csvFile)
            outEntry.delete(0, END)
            outEntry.insert(0, csvFile.rstrip(".csv")+".png")


    #Browse Output File Function
        def browseOut():
            csvOut = filedialog.asksaveasfilename(**self.browseOut_opt)
            outEntry.delete(0, END)
            outEntry.insert(0, csvOut)

    #Setup Desired File
        def get_csv_filenames(path):
            return [csvEntry.get()]

    #Read Desired File
        def read_csv_file(path):
            with open(path) as csv_file:
                return [row for row in reader(csv_file, delimiter=",")]

    #Determine X Axis
        def x_axis(headers):
            str_dates = [date.split(" ")[0] for date in headers[1:]]
            date_objs = [datetime.strptime(date, "%d/%m/%Y") for
                                date in str_dates]
            date_objs.sort()
            return np.array(date_objs, dtype=object)

    #Determine Y Axis
        def y_axis(data):
            return [float(row[0]) for row in data[1:]]

    #Determine Z Axis
        def z_data(data):
            return np.array([row[1:] for row in data[1:]], dtype=np.float64)

    #Generate Plot
        def generate_plot(x, y, z):
            fig = plt.figure(figsize=(5, 3), dpi=250)
            # print(max(new_x)/len(new_x))
            #new_y = np.arange(min(y), max(y), (max(y)-min(y))/len(y))
            #print(y)
            #print(new_y)
            #plt.imshow(z, interpolation='bilinear', cmap=cm.RdYlGn)
            colour_plot = plt.contourf(x, y, z, methodVar.get(),
                                            cmap=gradientVar.get())
            key = plt.colorbar(colour_plot)
            key.ax.set_ylabel("Inclination")
            plt.title(titleEntry.get())
            fig.autofmt_xdate()
            plt.tick_params(axis="x", labelsize=8)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
            plt.ylabel("Depth (m)")
            plt.gca().invert_yaxis()
            fig.set_tight_layout(True)
            return plt

    #Define Plot
        def plot(file):
            data = read_csv_file(file)
            contour = generate_plot(
                x_axis(data[0]),
                y_axis(data),
                z_data(data)
            )
            contour.savefig(outEntry.get(), dpi=250)

    #Main Instruction
        def graphGo():
            if __name__ == "__main__":
                if args.input:
                    plot(args.input)
                else:
                    script_path = dirname(abspath(__file__))
                    chdir(script_path)
                    [plot(file) for file in get_csv_filenames(".")]
                    plt.show(outEntry.get())

# ============================================================================ #
# OPTIONS
# ============================================================================ #
    #Browse Options
        self.browse_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('csv files', '.csv')]

    #Browse Output Options
        self.browseOut_opt = options = {}
        options['defaultextension'] = '.png'
        options['filetypes'] = [('png files', '.png')]

    #Font Options/Styles
        Font="Courier", 9
        Title="Courier", 20, 'underline'

    #Rules For GUI Spacing
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

# ============================================================================ #
# GUI LAYOUT
# ============================================================================ #
    #Title
        Ltitle=Label(self, text='Inclinometer Contour Modeling', font=Title,
                        width=35)
        Ltitle.grid(row=0, columnspan=10)

    #CSV Entry & Selection
        csvTitle=Label(self,text="CSV Input File", font=(Font),width=17)
        csvTitle.grid(row=1,column=0)

        csvEntryVar=StringVar()
        csvEntry=Entry(self,textvariable=csvEntryVar, width=50)
        csvEntry.grid(row=1,column=1, columnspan=8)

        csvBrowse=Button(self,text="Browse", font=Font, width=10,command=browse)
        csvBrowse.grid(row=1,column=9)

    #Graph Title
        outTitle=Label(self,text="Graph Title", font=(Font),width=17)
        outTitle.grid(row=4,column=0)

        titleEntry_value=StringVar()
        titleEntry=Entry(self,textvariable=titleEntry_value, width=50)
        titleEntry.grid(row=4,column=1, columnspan=8)
        titleEntry.insert(END, "Inclinometer Contour Plot")

    #InterpVariables
        interpText=Label(self, text='Resolution', font=(Font), width=17)
        interpText.grid(row=5, column=0)

        methodVar=IntVar(value=10)
        radioMethod1=Radiobutton(self, text='Default', font=(Font),
                                        variable=methodVar, value=10)
        radioMethod1.place(relx=.335, rely=0.47, anchor="c")

        radioMethod2=Radiobutton(self, text='Double', font=(Font),
                                        variable=methodVar, value=25)
        radioMethod2.place(relx=.535, rely=0.47, anchor="c")

        radioMethod3=Radiobutton(self, text='Squared', font=(Font),
                                        variable=methodVar, value=100)
        radioMethod3.place(relx=.735, rely=0.47, anchor="c")

        radioMethod4=Radiobutton(self, text='Halved', font=(Font),
                                        variable=methodVar, value=5)
        radioMethod4.place(relx=.935, rely=0.47, anchor="c")

    #ColourGradientChoice
        colourText=Label(self, text='Colour/Gradient', font=(Font), width=17)
        colourText.grid(row=6, column=0)

        gradientVar=StringVar(value='jet')
        radioGradient1=Radiobutton(self, text='Default', font=(Font),
                                        variable=gradientVar, value='jet')
        radioGradient1.place(relx=.335, rely=0.59, anchor="c")

        radioGradient2=Radiobutton(self, text='Diverge', font=(Font),
                                        variable=gradientVar, value='coolwarm')
        radioGradient2.place(relx=.535, rely=0.59, anchor="c")

        radioGradient3=Radiobutton(self, text='Autumn', font=(Font),
                                        variable=gradientVar, value='YlOrRd')
        radioGradient3.place(relx=.735, rely=0.59, anchor="c")

        radioGradient4=Radiobutton(self, text='Greys', font=(Font),
                                        variable=gradientVar, value='gray_r')
        radioGradient4.place(relx=.935, rely=0.59, anchor="c")

    #Output Distination
        outTitle=Label(self,text="Output Location", font=(Font),width=17)
        outTitle.grid(row=8,column=0)

        outEntry_value=StringVar()
        outEntry=Entry(self,textvariable=outEntry_value, width=50)
        outEntry.grid(row=8,column=1, columnspan=8)

        outBrowse=Button(self,text="Browse", font=Font, width=10,
                                command=browseOut)
        outBrowse.grid(row=8,column=9)

    #Go Button
        graphGo=Button(self, text="Generate Contour Graph", font=Font, width=72,
                                command=graphGo)
        graphGo.grid(row=9,columnspan=10)

    #Feedback Text
        statusText = StringVar(root)
        statusText.set("Press Browse button or enter CSV file directory, "
                    "then press the Go button")
        feedback=Label(self, textvariable=statusText)
        feedback.grid(row=10, columnspan=10)

# ============================================================================ #
# ARGUMENTS
# ============================================================================ #
        parser = ArgumentParser()
        parser.add_argument("-i", "--input", help="TXT file with input values",
                            type=str)
        args = parser.parse_args()

# ============================================================================ #
# OPT LOOP
# ============================================================================ #

if __name__ == '__main__':
    root = Tk()
    root.title("Inclinometer Contour Modeling")
    root.geometry("600x540")
    app = window(root)
    root.mainloop()
