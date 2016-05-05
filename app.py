from ui.mainwindow import *

# for testing:
leftFile = os.getcwd() + os.path.sep + 'left.txt'
rightFile = os.getcwd() + os.path.sep + 'right.txt'

main_window = MainWindow()
main_window.start(leftFile, rightFile)