import os
from difflibparser.difflibparser import *
from ui.mainwindow_ui import MainWindowUI
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory

class MainWindow:
    def start(self, leftFile = None, rightFile = None):
        self.main_window = Tk()
        self.main_window.title('Difftools')
        self.main_window_ui = MainWindowUI(self.main_window)

        self.main_window_ui.center_window()
        # self.main_window_ui.create_browse_buttons(lambda:self.load_file('left'), lambda:self.load_file('right'))
        self.main_window_ui.create_file_path_labels()
        self.main_window_ui.create_text_areas()
        self.main_window_ui.create_line_numbers()
        self.main_window_ui.create_scroll_bars()
        self.main_window_ui.create_file_treeview()
        path_to_my_project = os.getcwd()
        self.browse_process_directory('', path_to_my_project, path_to_my_project)
        self.main_window_ui.add_menu('File', [
            {'name': 'Compare Files', 'command': self.browse_files},
            {'name': 'Compare Directories', 'command': self.browse_directories},
            {'separator'},
            {'name': 'Exit', 'command': self.exit}
            ])

        if leftFile != None:
            self.leftFileContents = open(leftFile).read()
            self.main_window_ui.leftFileLabel.config(text=leftFile)

        if rightFile != None:
            self.rightFileContents = open(rightFile).read()
            self.main_window_ui.rightFileLabel.config(text=rightFile)

        self.fill_text_and_highlight_diffs()
        self.main_window.mainloop()

    def browse_files(self):
        self.load_file('left')
        self.load_file('right')

    # Load directories into the treeview
    def browse_directories(self):
        leftDir = self.load_directory('left')
        rightDir = self.load_directory('right')
        self.main_window_ui.fileTreeView.delete(*self.main_window_ui.fileTreeView.get_children())
        self.browse_process_directory('', leftDir, rightDir)
        self.fill_text_and_highlight_diffs()

    # Recursive method to fill the treevie with given directory hierarchy
    def browse_process_directory(self, parent, leftPath, rightPath):
        if parent == '':
            leftDirName = os.path.basename(leftPath)
            rightDirName = os.path.basename(rightPath)
            self.main_window_ui.fileTreeView.heading('#0', text=leftDirName + ' / ' + rightDirName, anchor=W)
        leftListing = os.listdir(leftPath)
        rightListing = os.listdir(rightPath)
        mergedListing = list(set(leftListing) | set(rightListing))
        for l in mergedListing:
            # Item in left dir only
            if l in leftListing and l not in rightListing:
                self.main_window_ui.fileTreeView.insert(parent, 'end', text=l, open=False, tags=('red'))
            # Item in right dir only
            elif l in rightListing and l not in leftListing:
                self.main_window_ui.fileTreeView.insert(parent, 'end', text=l, open=False, tags=('green'))
            # Item in both dirs
            else:
                newLeftPath = os.path.join(leftPath, l)
                newRightPath = os.path.join(rightPath, l)
                if (not os.path.isdir(newLeftPath) and os.path.isdir(newRightPath)) or (os.path.isdir(newLeftPath) and not os.path.isdir(newRightPath)):
                    self.main_window_ui.fileTreeView.insert(parent, 'end', text=l, open=False, tags=('yellow'))
                else:
                    # Diff the two files to either show them in white or yellow
                    # For now, show them in white
                    oid = self.main_window_ui.fileTreeView.insert(parent, 'end', text=l, open=False)
                    if os.path.isdir(newLeftPath) and os.path.isdir(newRightPath):
                        self.browse_process_directory(oid, newLeftPath, newRightPath)

    def load_file(self, pos):
        fname = askopenfilename()
        if fname:
            if pos == 'left':
                self.leftFileContents = open(fname).read()
                self.main_window_ui.leftFileLabel.config(text=fname)
            else:
                self.rightFileContents = open(fname).read()
                self.main_window_ui.rightFileLabel.config(text=fname)
            self.fill_text_and_highlight_diffs()

    def load_directory(self, pos):
        fname = askdirectory()
        if fname:
            if pos == 'left':
                self.main_window_ui.leftFileLabel.config(text=fname)
            else:
                self.main_window_ui.rightFileLabel.config(text=fname)
        return fname

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

        diff = DifflibParser(self.leftFileContents.splitlines(), self.rightFileContents.splitlines())

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

    def exit(self):
        self.main_window.destroy()
