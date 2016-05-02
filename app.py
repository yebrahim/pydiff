from ui.mainwindow import *

# for testing:
leftFile = os.getcwd() + os.path.sep + 'left.txt'
rightFile = os.getcwd() + os.path.sep + 'right.txt'
leftFileLines = open(leftFile).read()
rightFileLines = open(rightFile).read()

main_window = MainWindow()
main_window.start(leftFileLines, rightFileLines)