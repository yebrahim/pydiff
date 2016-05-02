import os
from difflibparser.difflibparser import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.font import Font
from linenumberswidget import TextWithLineNumbers
from linenumberswidget import LineNumbersCanvas

class MainWindow:
    def start(self, leftLines = '', rightLines = ''):
        self.leftFileLines = leftLines
        self.rightFileLines = rightLines

        self.main_window = Tk()
        self.main_window.title('Difftools')
        self.create_window_widgets()

        # Center window
        sw = self.main_window.winfo_screenwidth()
        sh = self.main_window.winfo_screenheight()

        w = 0.5 * sw
        h = 0.5 * sh

        x = (sw - w)/2
        y = (sh - h)/2
        self.main_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.fill_text_and_highlight_diffs()
        self.main_window.mainloop()

    def create_window_widgets(self):
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
        leftFileButton = Button(self.main_window, text='Browse', command=lambda:self.load_file('left'), width=10)
        leftFileButton.grid(row=browseButtonsRow, column=leftBrowseButtonsCol, sticky=W, columnspan=2)
        rightFileButton = Button(self.main_window, text='Browse', command=lambda:self.load_file('right'), width=10)
        rightFileButton.grid(row=browseButtonsRow, column=rightBrowseButtonsCol, sticky=W, columnspan=2)

        # Labels
        self.leftFileLabel = Label(self.main_window, text='Left file: ')
        self.leftFileLabel.grid(row=filePathLabelsRow, column=leftFilePathLabelsCol, sticky=W, columnspan=2)
        self.rightFileLabel = Label(self.main_window, text='Right file: ')
        self.rightFileLabel.grid(row=filePathLabelsRow, column=rightFilePathLabelsCol, sticky=W, columnspan=2)

        # Text areas
        regular_font = Font(family='Consolas', size=10)

        self.leftFileTextArea = TextWithLineNumbers(self.main_window, padx=5, pady=5, width=1, height=1)
        self.leftFileTextArea.grid(row=textAreasRow, column=leftTextAreaCol, sticky=N+E+S+W)
        self.leftFileTextArea.config(font=regular_font)
        self.leftFileTextArea.config(wrap='none')

        self.rightFileTextArea = TextWithLineNumbers(self.main_window, padx=5, pady=5, width=1, height=1)
        self.rightFileTextArea.grid(row=textAreasRow, column=rightTextAreaCol, sticky=N+S+E+W)
        self.rightFileTextArea.config(font=regular_font)
        self.rightFileTextArea.config(wrap='none')

        # Line numbers
        leftLinenumbers = LineNumbersCanvas(self.main_window, width=30)
        leftLinenumbers.attach(self.leftFileTextArea)
        leftLinenumbers.grid(row=lineNumbersRow, column=leftLineNumbersCol, sticky=N+S)
        self.leftFileTextArea.bind('<<Change>>', leftLinenumbers.redraw)
        self.leftFileTextArea.bind('<Configure>', leftLinenumbers.redraw)

        rightLinenumbers = LineNumbersCanvas(self.main_window, width=30)
        rightLinenumbers.attach(self.rightFileTextArea)
        rightLinenumbers.grid(row=lineNumbersRow, column=rightLineNumbersCol, sticky=N+S)
        self.rightFileTextArea.bind('<<Change>>', rightLinenumbers.redraw)
        self.rightFileTextArea.bind('<Configure>', rightLinenumbers.redraw)

        # configuring a tag called diff
        self.leftFileTextArea.tag_configure('red', background='#ff9494')
        self.leftFileTextArea.tag_configure('darkred', background='#ff0000')
        self.leftFileTextArea.tag_configure('gray', background='#cccccc')
        self.rightFileTextArea.tag_configure('green', background='#94ffaf')
        self.rightFileTextArea.tag_configure('darkgreen', background='#269141')
        self.rightFileTextArea.tag_configure('gray', background='#cccccc')

        self.leftFileTextArea.config(state=DISABLED)
        self.rightFileTextArea.config(state=DISABLED)

        self.uniScrollbar = Scrollbar(self.main_window)
        self.uniScrollbar.grid(row=uniScrollbarRow, column=uniScrollbarCol, stick=N+S)
        self.uniScrollbar.config(command=self.scrollBoth)
        self.leftFileTextArea.config(yscrollcommand=self.updateScroll)
        self.rightFileTextArea.config(yscrollcommand=self.updateScroll)

        leftHorizontalScrollbar = Scrollbar(self.main_window, orient=HORIZONTAL)
        leftHorizontalScrollbar.grid(row=horizontalScrollbarRow, column=leftHorizontalScrollbarCol, stick=E+W)
        leftHorizontalScrollbar.config(command=self.leftFileTextArea.xview)
        self.leftFileTextArea.config(xscrollcommand=leftHorizontalScrollbar.set)

        rightHorizontalScrollbar = Scrollbar(self.main_window, orient=HORIZONTAL)
        rightHorizontalScrollbar.grid(row=horizontalScrollbarRow, column=rightHorizontalScrollbarCol, stick=E+W)
        rightHorizontalScrollbar.config(command=self.rightFileTextArea.xview)
        self.rightFileTextArea.config(xscrollcommand=rightHorizontalScrollbar.set)

        self.main_window.grid_rowconfigure(textAreasRow, weight=1)
        self.main_window.grid_columnconfigure(leftTextAreaCol, weight=1)
        self.main_window.grid_columnconfigure(rightTextAreaCol, weight=1)

        for child in self.main_window.winfo_children(): child.grid_configure(padx=5, pady=5)

    # self.uniScrollbar
    def scrollBoth(self, action, position, type=None):
        self.leftFileTextArea.yview_moveto(position)
        self.rightFileTextArea.yview_moveto(position)

    def updateScroll(self, first, last, type=None):
        self.leftFileTextArea.yview_moveto(first)
        self.rightFileTextArea.yview_moveto(first)
        self.uniScrollbar.set(first, last)

    def load_file(self, pos):
        fname = askopenfilename()
        if fname:
            if pos == 'left':
                self.leftFileLines = open(fname).read()
                self.leftFileLabel.config(text=fname)
            else:
                self.rightFileLines = open(fname).read()
                self.rightFileLabel.config(text=fname)
            self.fill_text_and_highlight_diffs()

    # Highlight characters in a line in the given text area
    def tag_line_chars(self, lineno, textArea, tag, charIdx=None):
        try:
            line_start = ''
            line_end = ''
            if charIdx:
                line_start = str(lineno + 1) + '.' + str(charIdx)
                line_end = str(lineno + 1) + '.' + str(charIdx + 1)
                textArea.tag_remove('red', line_start, line_end)
            else:
                line_start = str(lineno + 1) + '.0'
                line_end = textArea.index('%s lineend' % line_start)
            textArea.tag_add(tag, line_start, line_end)
        except TclError as e:
            showerror('problem', str(e))

    # Highlight diff tags
    def fill_text_and_highlight_diffs(self):

        # enable text area edits so we can clear and insert into them
        self.leftFileTextArea.config(state=NORMAL)
        self.rightFileTextArea.config(state=NORMAL)

        diff = DifflibParser(self.leftFileLines.splitlines(), self.rightFileLines.splitlines())

        self.leftFileTextArea.delete(1.0, END)
        self.rightFileTextArea.delete(1.0, END)

        lineno = 0
        for line in diff:
            if line['code'] == DiffCode.SIMILAR:
                self.leftFileTextArea.insert('end', line['line'] + '\n')
                self.rightFileTextArea.insert('end', line['line'] + '\n')
            elif line['code'] == DiffCode.RIGHTONLY:
                self.leftFileTextArea.insert('end', '\n', 'gray')
                self.rightFileTextArea.insert('end', line['line'] + '\n', 'green')
            elif line['code'] == DiffCode.LEFTONLY:
                self.leftFileTextArea.insert('end', line['line'] + '\n', 'red')
                self.rightFileTextArea.insert('end', '\n', 'gray')
            elif line['code'] == DiffCode.CHANGED:
                for (i,c) in enumerate(line['line']):
                    self.leftFileTextArea.insert('end', c, 'darkred' if i in line['leftchanges'] else 'red')
                for (i,c) in enumerate(line['newline']):
                    self.rightFileTextArea.insert('end', c, 'darkgreen' if i in line['rightchanges'] else 'green')
                self.leftFileTextArea.insert('end', '\n')
                self.rightFileTextArea.insert('end', '\n')

        self.leftFileTextArea.config(state=DISABLED)
        self.rightFileTextArea.config(state=DISABLED)