from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

root = Tk()
root.title("Difftools")

leftFile = StringVar()
rightFile = StringVar()

def load_file(pos):
    fname = askopenfilename()
    if fname:
        try:
            text = open(fname).read()
            if pos == 'right':
                rightFile.set(fname)
                rightFileText.insert(1.0, text)
            else:
                leftFile.set(fname)
                leftFileText.insert(1.0, text)
            print(pos, " ", fname)
        except:                     # <- naked except is a bad idea
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

# Buttons
leftFileButton = Button(root, text="Browse", command=lambda:load_file("left"), width=10)
leftFileButton.grid(row=1, column=0, sticky=W)
rightFileButton = Button(root, text="Browse", command=lambda:load_file("right"), width=10)
rightFileButton.grid(row=1, column=2, sticky=W)

# Labels
leftFileLabel = Label(root, text="Left file: ")
leftFileLabel.grid(row=2, column=0, sticky=W)
rightFileLabel = Label(root, text="Right file: ")
rightFileLabel.grid(row=2, column=2, sticky=W)

# Text areas
leftFileText = Text(root, padx=5, pady=5, width=1, height=1)
leftFileText.grid(row=3, column=0, sticky=N+E+S+W)
rightFileText = Text(root, padx=5, pady=5, width=1, height=1)
rightFileText.grid(row=3, column=2, sticky=(N,S,E,W))

# Scrollbars
leftScrollbar = Scrollbar(root)
leftScrollbar.grid(row=3, column=1, stick=N+S)
leftScrollbar.config(command=leftFileText.yview)
leftFileText.config(yscrollcommand=leftScrollbar.set)

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

for child in root.winfo_children(): child.grid_configure(padx=5, pady=5)

# Center window
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

w = 0.5 * sw
h = 0.5 * sh

x = (sw - w)/2
y = (sh - h)/2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.mainloop()
