from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.font import Font
import os
import difflib

root = Tk()
root.title("Difftools")

def load_file_to_text_area(fname, textArea):
    textArea.config(state=NORMAL)
    try:
        text = open(fname).read()
        textArea.delete(1.0, END) 
        textArea.insert(1.0, text)
    except Exception as e:
        showerror("Open Source File", "Failed to read file\n'%s'. Error: %s" % (fname, e))
    finally:
        textArea.config(state=DISABLED)

def load_file(pos):
    fname = askopenfilename()
    if fname:
        if pos == 'right':
            load_file_to_text_area(fname, rightFileTextArea)
        else:
            load_file_to_text_area(fname, leftFileTextArea)
        highlight_diffs()

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
regular_font = Font(family="Consolas", size=10)

leftFileTextArea = Text(root, padx=5, pady=5, width=1, height=1)
leftFileTextArea.grid(row=3, column=0, sticky=N+E+S+W)
leftFileTextArea.config(font=regular_font)
leftFileTextArea.config(wrap="none")

rightFileTextArea = Text(root, padx=5, pady=5, width=1, height=1)
rightFileTextArea.grid(row=3, column=2, sticky=(N,S,E,W))
rightFileTextArea.config(font=regular_font)
rightFileTextArea.config(wrap="none")

# Highlight characters in a line in the given text area
def tag_line_chars(lineno, textArea, tag, charIdx=None):
    try:
        line_start = ""
        line_end = ""
        if charIdx:
            line_start = str(lineno + 1) + "." + str(charIdx)
            line_end = str(lineno + 1) + "." + str(charIdx + 1)
            textArea.tag_remove("red", line_start, line_end)
        else:
            line_start = str(lineno + 1) + ".0"
            line_end = textArea.index("%s lineend" % line_start)
        textArea.tag_add(tag, line_start, line_end)
    except TclError as e:
        showerror("problem", str(e))

# Highlight diff tags
def highlight_diffs():
    leftString = leftFileTextArea.get("1.0",END)
    rightString = rightFileTextArea.get("1.0",END)
    diff = difflib.ndiff(leftString.splitlines(), rightString.splitlines())
    lineno = 0
    # print("-------------\n",'\n'.join(diff),"\n--------------")
    sawMinus = sawPlus = sawQ = False
    for line in diff:
        code = line[:2]
        # print("diff line # %d: %s" % (lineno, line))
        if code == '- ':
            sawMinus = True
            tag_line_chars(lineno, leftFileTextArea, "red")
            # tag_line_chars(lineno, rightFileTextArea, "green")
        elif code == '+ ':
            sawPlus = True
            # tag_line_chars(lineno, leftFileTextArea, "red")
            tag_line_chars(lineno, rightFileTextArea, "green")
        if code == '? ':
            sawQ = True
            # highlight individual characters
            minusIndices = [i - 2 for (i,c) in enumerate(line) if c == '-']
            for i in minusIndices:
                tag_line_chars(lineno, leftFileTextArea, "darkred", i)
            plusIndices = [i - 2 for (i,c) in enumerate(line) if c == '+']
            for i in plusIndices:
                tag_line_chars(lineno, rightFileTextArea, "darkgreen", i)
        if code == '  ' or (sawMinus and sawPlus and sawQ):
            lineno += 1
            sawMinus = sawPlus = sawQ = False

# for testing:
leftFile = os.getcwd() + os.path.sep + 'left.txt'
rightFile = os.getcwd() + os.path.sep + 'right.txt'
load_file_to_text_area(leftFile, leftFileTextArea)
load_file_to_text_area(rightFile, rightFileTextArea)

# configuring a tag called diff
leftFileTextArea.tag_configure("red", background="#ff9494")
leftFileTextArea.tag_configure("darkred", background="#ff0000")
rightFileTextArea.tag_configure("green", background="#94ffaf")
rightFileTextArea.tag_configure("darkgreen", background="#269141")
highlight_diffs()

leftFileTextArea.config(state=DISABLED)
rightFileTextArea.config(state=DISABLED)

# UniScrollbar
def scrollBoth(action, position, type=None):
    leftFileTextArea.yview_moveto(position)
    rightFileTextArea.yview_moveto(position)

def updateScroll(first, last, type=None):
    leftFileTextArea.yview_moveto(first)
    rightFileTextArea.yview_moveto(first)
    uniScrollbar.set(first, last)

uniScrollbar = Scrollbar(root)
uniScrollbar.grid(row=3, column=1, stick=N+S)
uniScrollbar.config(command=scrollBoth)
leftFileTextArea.config(yscrollcommand=updateScroll)
rightFileTextArea.config(yscrollcommand=updateScroll)

leftHorizontalScrollbar = Scrollbar(root, orient=HORIZONTAL)
leftHorizontalScrollbar.grid(row=4, column=0, stick=E+W)
leftHorizontalScrollbar.config(command=leftFileTextArea.xview)
leftFileTextArea.config(xscrollcommand=leftHorizontalScrollbar.set)

rightHorizontalScrollbar = Scrollbar(root, orient=HORIZONTAL)
rightHorizontalScrollbar.grid(row=4, column=2, stick=E+W)
rightHorizontalScrollbar.config(command=rightFileTextArea.xview)
rightFileTextArea.config(xscrollcommand=rightHorizontalScrollbar.set)

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
