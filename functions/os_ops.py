import os
import subprocess as sp

paths={
    'notepad':"C:\\Windows\\System32\\notepad.exe",
    'git':'C:\\Program Files\\Git\\git-bash.exe',
    'calculator': "C:\\Windows\\System32\\calc.exe"   
}

def open_notepad():
    os.startfile(paths['notepad'])

def open_git():
    os.startfile(paths['git'])

def open_cmd():
    os.system('start cmd')

def open_camera():
    sp.run('start microsoft.windows.camera:',shell=True)

def open_calculator():
    sp.Popen(paths['calculator'])