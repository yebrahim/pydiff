from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showerror
from tkinter.font import Font
from ui.linenumberswidget import TextWithLineNumbers
from ui.linenumberswidget import LineNumbersCanvas
import os

class MainWindowUI:

    # Rows
    browseButtonsRow = 0
    fileTreeRow = filePathLabelsRow = 1
    uniScrollbarRow = lineNumbersRow = textAreasRow = 2
    horizontalScrollbarRow = 3

    # Columns
    fileTreeCol = 0
    fileTreeScrollbarCol = 1
    leftLineNumbersCol = 2
    leftBrowseButtonsCol = leftFilePathLabelsCol = 2    # should span at least two columns
    leftTextAreaCol = leftHorizontalScrollbarCol = 3
    uniScrollbarCol = 4
    rightLineNumbersCol = 5
    rightBrowseButtonsCol = rightFilePathLabelsCol = 6  # should span at least two columns
    rightTextAreaCol = rightHorizontalScrollbarCol = 6

    # Colors
    whiteColor = '#ffffff'
    redColor = '#ff9494'
    darkredColor = '#ff0000'
    grayColor = '#cccccc'
    greenColor = '#94ffaf'
    darkgreenColor = '#269141'
    yellowColor = '#f0f58c'

    def __init__(self, window):
        self.main_window = window
        self.main_window.grid_rowconfigure(self.filePathLabelsRow, weight=0)
        self.main_window.grid_rowconfigure(self.textAreasRow, weight=1)
        self.main_window.grid_columnconfigure(self.leftTextAreaCol, weight=1)
        self.main_window.grid_columnconfigure(self.rightTextAreaCol, weight=1)
        self.menubar = Menu(self.main_window)
        self.menus = {}

    # Center window and set its size
    def center_window(self):
        sw = self.main_window.winfo_screenwidth()
        sh = self.main_window.winfo_screenheight()

        w = 0.5 * sw
        h = 0.5 * sh

        x = (sw - w)/2
        y = (sh - h)/2
        self.main_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Menu bar
    def add_menu(self, menuName, commandList):
        self.menus[menuName] = Menu(self.menubar,tearoff=0)
        for c in commandList:
            if 'separator' in c: self.menus[menuName].add_separator()
            else: self.menus[menuName].add_command(label=c['name'], command=c['command'])
        self.menubar.add_cascade(label=menuName, menu=self.menus[menuName])
        self.main_window.config(menu=self.menubar)

    # Buttons
    def create_browse_buttons(self, leftLoadButtonCallback, rightLoadButtonCallback):
        self.leftFileButton = Button(self.main_window, text='Browse', command=leftLoadButtonCallback, width=10)
        self.leftFileButton.grid(row=self.browseButtonsRow, column=self.leftBrowseButtonsCol, sticky=W, columnspan=2)
        self.rightFileButton = Button(self.main_window, text='Browse', command=rightLoadButtonCallback, width=10)
        self.rightFileButton.grid(row=self.browseButtonsRow, column=self.rightBrowseButtonsCol, sticky=W, columnspan=2)

    # Labels
    def create_file_path_labels(self):
        self.leftFileLabel = Label(self.main_window, text='Left file: ')
        self.leftFileLabel.grid(row=self.filePathLabelsRow, column=self.leftFilePathLabelsCol, columnspan=2)
        self.rightFileLabel = Label(self.main_window, text='Right file: ')
        self.rightFileLabel.grid(row=self.filePathLabelsRow, column=self.rightFilePathLabelsCol, columnspan=2)

    # File treeview
    def create_file_treeview(self):
        self.fileTreeView = Treeview(self.main_window)
        ysb = Scrollbar(self.main_window, orient='vertical', command=self.fileTreeView.yview)
        xsb = Scrollbar(self.main_window, orient='horizontal', command=self.fileTreeView.xview)
        self.fileTreeView.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.fileTreeView.grid(row=self.fileTreeRow, column=self.fileTreeCol, sticky=NS, rowspan=2)
        ysb.grid(row=self.fileTreeRow, column=self.fileTreeScrollbarCol, sticky=NS, rowspan=2)
        xsb.grid(row=self.horizontalScrollbarRow, column=self.fileTreeCol, sticky=EW)

        self.fileTreeView.tag_configure('red', background=self.redColor)
        self.fileTreeView.tag_configure('green', background=self.greenColor)
        self.fileTreeView.tag_configure('yellow', background=self.yellowColor)

    # Text areas
    def create_text_areas(self):
        regular_font = Font(family='Consolas', size=10)

        self.leftFileTextArea = TextWithLineNumbers(self.main_window, padx=5, pady=5, width=1, height=1, bg=self.grayColor)
        self.leftFileTextArea.grid(row=self.textAreasRow, column=self.leftTextAreaCol, sticky=NSEW)
        self.leftFileTextArea.config(font=regular_font)
        self.leftFileTextArea.config(wrap='none')

        self.rightFileTextArea = TextWithLineNumbers(self.main_window, padx=5, pady=5, width=1, height=1, bg=self.grayColor)
        self.rightFileTextArea.grid(row=self.textAreasRow, column=self.rightTextAreaCol, sticky=NSEW)
        self.rightFileTextArea.config(font=regular_font)
        self.rightFileTextArea.config(wrap='none')

        # configuring highlight tags
        self.leftFileTextArea.tag_configure('red', background=self.redColor)
        self.leftFileTextArea.tag_configure('darkred', background=self.darkredColor)
        self.leftFileTextArea.tag_configure('gray', background=self.grayColor)
        self.rightFileTextArea.tag_configure('green', background=self.greenColor)
        self.rightFileTextArea.tag_configure('darkgreen', background=self.darkgreenColor)
        self.rightFileTextArea.tag_configure('gray', background=self.grayColor)

        # disable the text areas
        self.leftFileTextArea.config(state=DISABLED)
        self.rightFileTextArea.config(state=DISABLED)

    # Line numbers
    def create_line_numbers(self):
        leftLinenumbers = LineNumbersCanvas(self.main_window, width=30)
        leftLinenumbers.attach(self.leftFileTextArea)
        leftLinenumbers.grid(row=self.lineNumbersRow, column=self.leftLineNumbersCol, sticky=NS)
        self.leftFileTextArea.bind('<<Change>>', leftLinenumbers.redraw)
        self.leftFileTextArea.bind('<Configure>', leftLinenumbers.redraw)

        rightLinenumbers = LineNumbersCanvas(self.main_window, width=30)
        rightLinenumbers.attach(self.rightFileTextArea)
        rightLinenumbers.grid(row=self.lineNumbersRow, column=self.rightLineNumbersCol, sticky=NS)
        self.rightFileTextArea.bind('<<Change>>', rightLinenumbers.redraw)
        self.rightFileTextArea.bind('<Configure>', rightLinenumbers.redraw)

    # Scroll bars

    def scrollBoth(self, action, position, type=None):
        self.leftFileTextArea.yview_moveto(position)
        self.rightFileTextArea.yview_moveto(position)

    def updateScroll(self, first, last, type=None):
        self.leftFileTextArea.yview_moveto(first)
        self.rightFileTextArea.yview_moveto(first)
        self.uniScrollbar.set(first, last)

    def create_scroll_bars(self):
        self.uniScrollbar = Scrollbar(self.main_window)
        self.uniScrollbar.grid(row=self.uniScrollbarRow, column=self.uniScrollbarCol, sticky=NS)
        self.uniScrollbar.config(command=self.scrollBoth)
        self.leftFileTextArea.config(yscrollcommand=self.updateScroll)
        self.rightFileTextArea.config(yscrollcommand=self.updateScroll)

        leftHorizontalScrollbar = Scrollbar(self.main_window, orient=HORIZONTAL)
        leftHorizontalScrollbar.grid(row=self.horizontalScrollbarRow, column=self.leftHorizontalScrollbarCol, sticky=EW)
        leftHorizontalScrollbar.config(command=self.leftFileTextArea.xview)
        self.leftFileTextArea.config(xscrollcommand=leftHorizontalScrollbar.set)

        rightHorizontalScrollbar = Scrollbar(self.main_window, orient=HORIZONTAL)
        rightHorizontalScrollbar.grid(row=self.horizontalScrollbarRow, column=self.rightHorizontalScrollbarCol, sticky=EW)
        rightHorizontalScrollbar.config(command=self.rightFileTextArea.xview)
        self.rightFileTextArea.config(xscrollcommand=rightHorizontalScrollbar.set)
