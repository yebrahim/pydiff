import os
from difflibparser.difflibparser import *
from ui.mainwindow_ui import MainWindowUI
from tkinter import *

class MainWindow:
    def start(self, leftLines = '', rightLines = ''):
        self.leftFileLines = leftLines
        self.rightFileLines = rightLines

        self.main_window = Tk()
        self.main_window.title('Difftools')
        self.main_window_ui = MainWindowUI(self.main_window)

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
        self.main_window_ui.leftFileTextArea.config(state=NORMAL)
        self.main_window_ui.rightFileTextArea.config(state=NORMAL)

        diff = DifflibParser(self.leftFileLines.splitlines(), self.rightFileLines.splitlines())

        self.main_window_ui.leftFileTextArea.delete(1.0, END)
        self.main_window_ui.rightFileTextArea.delete(1.0, END)

        lineno = 0
        for line in diff:
            if line['code'] == DiffCode.SIMILAR:
                self.main_window_ui.leftFileTextArea.insert('end', line['line'] + '\n')
                self.main_window_ui.rightFileTextArea.insert('end', line['line'] + '\n')
            elif line['code'] == DiffCode.RIGHTONLY:
                self.main_window_ui.leftFileTextArea.insert('end', '\n', 'gray')
                self.main_window_ui.rightFileTextArea.insert('end', line['line'] + '\n', 'green')
            elif line['code'] == DiffCode.LEFTONLY:
                self.main_window_ui.leftFileTextArea.insert('end', line['line'] + '\n', 'red')
                self.main_window_ui.rightFileTextArea.insert('end', '\n', 'gray')
            elif line['code'] == DiffCode.CHANGED:
                for (i,c) in enumerate(line['line']):
                    self.main_window_ui.leftFileTextArea.insert('end', c, 'darkred' if i in line['leftchanges'] else 'red')
                for (i,c) in enumerate(line['newline']):
                    self.main_window_ui.rightFileTextArea.insert('end', c, 'darkgreen' if i in line['rightchanges'] else 'green')
                self.main_window_ui.leftFileTextArea.insert('end', '\n')
                self.main_window_ui.rightFileTextArea.insert('end', '\n')

        self.main_window_ui.leftFileTextArea.config(state=DISABLED)
        self.main_window_ui.rightFileTextArea.config(state=DISABLED)