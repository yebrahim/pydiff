"""
MIT License

Copyright (c) 2016 Yasser Elsayed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:    # for Python2
    from Tkinter import *
except ImportError:    # for Python3
    from tkinter import *

class SearchTextDialog(Frame):

    def __init__(self, parent, textwidgets, searchButtonCallback):
        Frame.__init__(self, parent)

        self.parent = parent
        self.__searchCallback = searchButtonCallback
        self.__textwidgets = textwidgets
        self.__searchStr = None
        self.initUI()

    def initUI(self):
        self.searchTextFrame = Frame(self.parent)

        self.searchTextEntry = Entry(self)
        self.searchTextEntry.pack(fill=BOTH, expand=True, side=LEFT)

        self.__matchCaseVar = IntVar()
        self.__matchCaseVar.set(0)
        self.searchTextCheckbutton = Checkbutton(self, text='Match case', variable=self.__matchCaseVar, command=lambda *x: self.clearSearch())
        self.searchTextCheckbutton.pack(side=LEFT, padx=10)

        self.searchTextButton = Button(self, text='Find', command=self.nextResult)
        self.searchTextButton.pack(side=LEFT)

        self.searchTextEntry.bind('<Return>', self.nextResult)
        self.searchTextButton.bind('<Return>', self.nextResult)
        self.__curSearchResult = {'term': None, 'indices': ['0.0'] * len(self.__textwidgets)}
        self.__insession = False

    def getSearchTerm(self):
        return self.searchTextEntry.get()

    def focus(self):
        self.searchTextEntry.focus_set()
        self.searchTextEntry.select_range(0, END)
        self.__insession = True

    def nextResult(self, *args):
        if not self.__insession: return

        searchStr = self.searchTextEntry.get()

        if not self.__searchStr or self.__searchStr != searchStr:
            self.__searchStr = searchStr
            self.__curSearchResult = {'term': searchStr, 'indices': ['0.0'] * len(self.__textwidgets)}

        if searchStr in ['', None]: return

        countVar = StringVar()
        for i,t in enumerate(self.__textwidgets):
            if self.__curSearchResult['indices'][i] == -1: continue
            nextIdx = float(self.__curSearchResult['indices'][i]) + 1
            pos = t.search(self.__searchStr, nextIdx, END, nocase=self.__matchCaseVar.get() == 0)
            self.__curSearchResult['indices'][i] = pos if pos else -1

        self.__searchCallback(self.__curSearchResult)

    def clearSearch(self):
        self.__curSearchResult['indices'] = ['0.0'] * len(self.__textwidgets)

    def unfocus(self):
        self.clearSearch()
        self.__insession = False
