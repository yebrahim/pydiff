# pydiff - A Minimalistic Difflib GUI
An open source Tkinter GUI for python's difflib comparing two text files or two directory trees, complete with highlighting of differences and line numbers.

<p align="center">
  <img src="https://github.com/yebrahim/python-difflib-gui/blob/master/screenshot.png" width="90%"/>
</p>

You can open File -> Compare Files to diff two text files, or choose File -> Compare Directories to diff directories. In the case of directories, the tool will show the directory structure in a tree sidebar to the left, and highlight files red if they're in left directory only, green if in the right one only, yellow if in both with changes, and white if in both with no changes.

The tool makes use of [this parser](https://github.com/yebrahim/difflibparser) that I wrote for python's difflib ndiff output, which converts the text output into diff objects that can be used in code.

## Requirements
pydiff works with stock Python2.7 and takes only one dependency on `tkinter`, which is built-in on MacOS so it should work out of the box. On Ubuntu, you can get it by running `sudo apt-get install python-tk`.

## Install
You can just clone the repo to your disk, just note that it uses a submodule, so you need to clone recursively:

`git clone --recursive https://github.com/yebrahim/pydiff.git`

Please open issues if you see any, and feel free to fix and send pull requests.

## Usage

`python pydiff.py`

You can also give it executable permissions and run it directly on unix systems:

`chmod +x pydiff.py`

`./pydiff.py`

To diff two paths directly (files or directories):

`python pydiff.py -p path1 path2`
