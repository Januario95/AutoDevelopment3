import time
import pywinauto
from pywinauto import mouse
from pywinauto import keyboard
from subprocess import Popen
from pywinauto import Desktop
from pywinauto.application import Application


app = Application().start(cmd_line='C:/Users/a248433/Documents/drivers/ChromeSetup.exe')
time.sleep(3)
window = app.Chrome_WidgetWin_1










# Popen('calc.exe', shell=True)
# dlg = Desktop(backend="uia").Calculator
# dlg.wait('visible')



# app = Application(backend="uia").start('notepad.exe')

# app = Application().start('chrome.exe --force-renderer-accessibility')

# app = Application(backend='uia').connect(path='chrome.exe', title_re='New Tab')

# describe the window inside Notepad.exe process
# dlg_spec = app.UntitledNotepad
# wait till the window is really open
# actionable_dlg = dlg_spec.wait('visible')



