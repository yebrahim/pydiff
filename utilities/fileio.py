from tkinter import *

class FileIO:
    def load_file_to_text_area(self, fname, textArea):
        textArea.config(state=NORMAL)
        try:
            text = open(fname).read()
            textArea.delete(1.0, END) 
            textArea.insert(1.0, text)
        except Exception as e:
            showerror('Open Source File', 'Failed to read file\n"%s". Error: %s' % (fname, e))
        finally:
            textArea.config(state=DISABLED)