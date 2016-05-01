import os, difflib
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.font import Font

from LineNumbersWidget import TextWithLineNumbers
from LineNumbersWidget import LineNumbersCanvas

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
        if pos == 'left':
            load_file_to_text_area(fname, leftFileTextArea)
            leftFileLabel.config(text=fname)
            leftLinenumbers.redraw()
        else:
            load_file_to_text_area(fname, rightFileTextArea)
            rightFileLabel.config(text=fname)
            # rightLinenumbers.redraw()
        highlight_diffs()

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
            print("diff line # %d: %s" % (lineno, line))
            sawMinus = True
            tag_line_chars(lineno, leftFileTextArea, "red")
            # rightFileTextArea.config(state=NORMAL)
            # rightFileTextArea.insert(str(lineno) + ".0", "\n")
            # rightFileTextArea.config(state=DISABLED)
        elif code == '+ ':
            print("diff line # %d: %s" % (lineno, line))
            sawPlus = True
            tag_line_chars(lineno, rightFileTextArea, "green")
            # leftFileTextArea.config(state=NORMAL)
            # leftFileTextArea.insert(str(lineno) + ".0", "\n")
            # leftFileTextArea.config(state=DISABLED)
        if code == '? ':
            print("diff line # %d: %s" % (lineno, line))
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

# Rows
browseButtonsRow = 0
filePathLabelsRow = 1
uniScrollbarRow = lineNumbersRow = textAreasRow = 2
horizontalScrollbarRow = 3

# Columns
leftLineNumbersCol = 0
leftBrowseButtonsCol = leftFilePathLabelsCol = 0    # should span at least two columns
leftTextAreaCol = leftHorizontalScrollbarCol = 1
uniScrollbarCol = 2
rightLineNumbersCol = 3
rightBrowseButtonsCol = rightFilePathLabelsCol = 4  # should span at least two columns
rightTextAreaCol = rightHorizontalScrollbarCol = 4

# Buttons
leftFileButton = Button(root, text="Browse", command=lambda:load_file("left"), width=10)
leftFileButton.grid(row=browseButtonsRow, column=leftBrowseButtonsCol, sticky=W, columnspan=2)
rightFileButton = Button(root, text="Browse", command=lambda:load_file("right"), width=10)
rightFileButton.grid(row=browseButtonsRow, column=rightBrowseButtonsCol, sticky=W, columnspan=2)

# Labels
leftFileLabel = Label(root, text="Left file: ")
leftFileLabel.grid(row=filePathLabelsRow, column=leftFilePathLabelsCol, sticky=W, columnspan=2)
rightFileLabel = Label(root, text="Right file: ")
rightFileLabel.grid(row=filePathLabelsRow, column=rightFilePathLabelsCol, sticky=W, columnspan=2)

# Text areas
regular_font = Font(family="Consolas", size=10)

leftFileTextArea = TextWithLineNumbers(root, padx=5, pady=5, width=1, height=1)
leftFileTextArea.grid(row=textAreasRow, column=leftTextAreaCol, sticky=N+E+S+W)
leftFileTextArea.config(font=regular_font)
leftFileTextArea.config(wrap="none")

rightFileTextArea = TextWithLineNumbers(root, padx=5, pady=5, width=1, height=1)
rightFileTextArea.grid(row=textAreasRow, column=rightTextAreaCol, sticky=N+S+E+W)
rightFileTextArea.config(font=regular_font)
rightFileTextArea.config(wrap="none")

# Line numbers
leftLinenumbers = LineNumbersCanvas(root, width=30)
leftLinenumbers.attach(leftFileTextArea)
leftLinenumbers.grid(row=lineNumbersRow, column=leftLineNumbersCol, sticky=N+S)
leftFileTextArea.bind("<<Change>>", leftLinenumbers.redraw)
leftFileTextArea.bind("<Configure>", leftLinenumbers.redraw)

rightLinenumbers = LineNumbersCanvas(root, width=30)
rightLinenumbers.attach(rightFileTextArea)
rightLinenumbers.grid(row=lineNumbersRow, column=rightLineNumbersCol, sticky=N+S)
rightFileTextArea.bind("<<Change>>", rightLinenumbers.redraw)
rightFileTextArea.bind("<Configure>", rightLinenumbers.redraw)

# configuring a tag called diff
leftFileTextArea.tag_configure("red", background="#ff9494")
leftFileTextArea.tag_configure("darkred", background="#ff0000")
rightFileTextArea.tag_configure("green", background="#94ffaf")
rightFileTextArea.tag_configure("darkgreen", background="#269141")

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
uniScrollbar.grid(row=uniScrollbarRow, column=uniScrollbarCol, stick=N+S)
uniScrollbar.config(command=scrollBoth)
leftFileTextArea.config(yscrollcommand=updateScroll)
rightFileTextArea.config(yscrollcommand=updateScroll)

leftHorizontalScrollbar = Scrollbar(root, orient=HORIZONTAL)
leftHorizontalScrollbar.grid(row=horizontalScrollbarRow, column=leftHorizontalScrollbarCol, stick=E+W)
leftHorizontalScrollbar.config(command=leftFileTextArea.xview)
leftFileTextArea.config(xscrollcommand=leftHorizontalScrollbar.set)

rightHorizontalScrollbar = Scrollbar(root, orient=HORIZONTAL)
rightHorizontalScrollbar.grid(row=horizontalScrollbarRow, column=rightHorizontalScrollbarCol, stick=E+W)
rightHorizontalScrollbar.config(command=rightFileTextArea.xview)
rightFileTextArea.config(xscrollcommand=rightHorizontalScrollbar.set)

root.grid_rowconfigure(textAreasRow, weight=1)
root.grid_columnconfigure(leftTextAreaCol, weight=1)
root.grid_columnconfigure(rightTextAreaCol, weight=1)

for child in root.winfo_children(): child.grid_configure(padx=5, pady=5)

# Center window
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

w = 0.5 * sw
h = 0.5 * sh

x = (sw - w)/2
y = (sh - h)/2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# for testing:
leftFile = os.getcwd() + os.path.sep + 'left.txt'
rightFile = os.getcwd() + os.path.sep + 'right.txt'
load_file_to_text_area(leftFile, leftFileTextArea)
load_file_to_text_area(rightFile, rightFileTextArea)
highlight_diffs()

root.mainloop()
