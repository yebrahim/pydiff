from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.font import Font
from linenumberswidget import TextWithLineNumbers
from linenumberswidget import LineNumbersCanvas

class MainWindowUI:

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

    def __init__(self, window):
        self.main_window = window
        self.main_window.grid_rowconfigure(self.textAreasRow, weight=1)
        self.main_window.grid_columnconfigure(self.leftTextAreaCol, weight=1)
        self.main_window.grid_columnconfigure(self.rightTextAreaCol, weight=1)

        self.create_browse_buttons()
        self.create_file_path_labels()
        self.create_text_areas()
        self.create_line_numbers()
        self.create_scroll_bars()

        for child in self.main_window.winfo_children(): child.grid_configure(padx=5, pady=5)

    # Menu bar
    def create_menu_bar(self):
        __thisMenuBar = Menu(__root)
        __thisFileMenu = Menu(__thisMenuBar,tearoff=0)
        __thisEditMenu = Menu(__thisMenuBar,tearoff=0)
        __thisHelpMenu = Menu(__thisMenuBar,tearoff=0)

    # Buttons
    def create_browse_buttons(self):
        leftFileButton = Button(self.main_window, text='Browse', command=lambda:self.load_file('left'), width=10)
        leftFileButton.grid(row=self.browseButtonsRow, column=self.leftBrowseButtonsCol, sticky=W, columnspan=2)
        rightFileButton = Button(self.main_window, text='Browse', command=lambda:self.load_file('right'), width=10)
        rightFileButton.grid(row=self.browseButtonsRow, column=self.rightBrowseButtonsCol, sticky=W, columnspan=2)

    # Labels
    def create_file_path_labels(self):
        self.leftFileLabel = Label(self.main_window, text='Left file: ')
        self.leftFileLabel.grid(row=self.filePathLabelsRow, column=self.leftFilePathLabelsCol, sticky=W, columnspan=2)
        self.rightFileLabel = Label(self.main_window, text='Right file: ')
        self.rightFileLabel.grid(row=self.filePathLabelsRow, column=self.rightFilePathLabelsCol, sticky=W, columnspan=2)

    # Text areas
    def create_text_areas(self):
        regular_font = Font(family='Consolas', size=10)

        self.leftFileTextArea = TextWithLineNumbers(self.main_window, padx=5, pady=5, width=1, height=1)
        self.leftFileTextArea.grid(row=self.textAreasRow, column=self.leftTextAreaCol, sticky=N+E+S+W)
        self.leftFileTextArea.config(font=regular_font)
        self.leftFileTextArea.config(wrap='none')

        self.rightFileTextArea = TextWithLineNumbers(self.main_window, padx=5, pady=5, width=1, height=1)
        self.rightFileTextArea.grid(row=self.textAreasRow, column=self.rightTextAreaCol, sticky=N+S+E+W)
        self.rightFileTextArea.config(font=regular_font)
        self.rightFileTextArea.config(wrap='none')

        # configuring highlight tags
        self.leftFileTextArea.tag_configure('red', background='#ff9494')
        self.leftFileTextArea.tag_configure('darkred', background='#ff0000')
        self.leftFileTextArea.tag_configure('gray', background='#cccccc')
        self.rightFileTextArea.tag_configure('green', background='#94ffaf')
        self.rightFileTextArea.tag_configure('darkgreen', background='#269141')
        self.rightFileTextArea.tag_configure('gray', background='#cccccc')

        # disable the text areas
        self.leftFileTextArea.config(state=DISABLED)
        self.rightFileTextArea.config(state=DISABLED)

    # Line numbers
    def create_line_numbers(self):
        leftLinenumbers = LineNumbersCanvas(self.main_window, width=30)
        leftLinenumbers.attach(self.leftFileTextArea)
        leftLinenumbers.grid(row=self.lineNumbersRow, column=self.leftLineNumbersCol, sticky=N+S)
        self.leftFileTextArea.bind('<<Change>>', leftLinenumbers.redraw)
        self.leftFileTextArea.bind('<Configure>', leftLinenumbers.redraw)

        rightLinenumbers = LineNumbersCanvas(self.main_window, width=30)
        rightLinenumbers.attach(self.rightFileTextArea)
        rightLinenumbers.grid(row=self.lineNumbersRow, column=self.rightLineNumbersCol, sticky=N+S)
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
        self.uniScrollbar.grid(row=self.uniScrollbarRow, column=self.uniScrollbarCol, stick=N+S)
        self.uniScrollbar.config(command=self.scrollBoth)
        self.leftFileTextArea.config(yscrollcommand=self.updateScroll)
        self.rightFileTextArea.config(yscrollcommand=self.updateScroll)

        leftHorizontalScrollbar = Scrollbar(self.main_window, orient=HORIZONTAL)
        leftHorizontalScrollbar.grid(row=self.horizontalScrollbarRow, column=self.leftHorizontalScrollbarCol, stick=E+W)
        leftHorizontalScrollbar.config(command=self.leftFileTextArea.xview)
        self.leftFileTextArea.config(xscrollcommand=leftHorizontalScrollbar.set)

        rightHorizontalScrollbar = Scrollbar(self.main_window, orient=HORIZONTAL)
        rightHorizontalScrollbar.grid(row=self.horizontalScrollbarRow, column=self.rightHorizontalScrollbarCol, stick=E+W)
        rightHorizontalScrollbar.config(command=self.rightFileTextArea.xview)
        self.rightFileTextArea.config(xscrollcommand=rightHorizontalScrollbar.set)
