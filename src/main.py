'''
@author: Mike
'''
import process
import gui

def setPath(path):
    p = process.Process()
    p.procWav(path)
    return p.beats, p.onset, p.notes
    
if __name__ == '__main__':
    app = gui.Gui(0)
    app.MainLoop()