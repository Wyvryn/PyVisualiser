from wx.glcanvas import *
from wxPython.wx import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import wx
import os 
import main
import time

beats= []
onset = []
notes = []
path = ""

class GuiFrame(wx.Frame):
    def __init__(self, parent, id, title):
        frm = wx.Frame.__init__(self, parent, id, title,
                                wx.DefaultPosition,(845, 710))
        
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(101, "&Select a File", "Select a file")
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.openfile, id=101)
        

    def openfile(self, event):
        global beats
        global onset
        global path
        global notes
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", 
                            wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.SetStatusText("You selected: %s" % path)
            beats, onset, notes = main.setPath(path)

        dlg.Destroy()
        

Near    = 1.0
Far     = 20.0

def drawCube (s1,s2,s3,s4,s5,s6,s7,s8,s9):
    glPushMatrix()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    color = [0.0,1.0,0.0,0.5]
    
    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glScalef(1,.5+s1,1)
    glutSolidCube(1)
    glPopMatrix()
    
    color = [1.0,0.,0.,.5]
    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(1.1,0,0)
    glScalef(1,.5+s2,1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(-1.1,0,0)
    glScalef(1,.5+s3,1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(0,0,1.1)
    glScalef(1,.5+s4,1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(0,0,-1.1)
    glScalef(1,.5+s5,1)
    glutSolidCube(1)
    glPopMatrix()
    
    color = [0.,0.,1.0,0.5]
    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(1.1,0,1.1)
    glScalef(1,.5+s6,1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(-1.1,0,1.1)
    glScalef(1,.5+s7,1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(1.1,0,-1.1)
    glScalef(1,.5+s8,1)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor4f(color[0], color[1], color[2], color[3])
    glTranslatef(-1.1,0,-1.1)
    glScalef(1,.5+s9,1)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
#
        
class myGLCanvas(GLCanvas):
    '''Actual OpenGL scene'''
    def __init__ (self, parent, attribs = None, id = wx.ID_ANY):
        if not attribs:
            attribs = [WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 24]
        GLCanvas.__init__(self, parent, id, attribList = attribs)
        self.init   = False
        self.width  = 0
        self.height = 0
        self.spin = 0.0
        self.startTime = 0
        self.setStart = False
        self.startAudio = False
        self.tick = 0
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Animation
        self.dir = 1
        self.s1 = 0.0
        self.s2 = 0.0
        self.s3 = 0.0
        self.s4 = 0.0
        self.s5 = 0.0
        self.s6 = 0.0
        self.s7 = 0.0
        self.s8 = 0.0
        self.s9 = 0.0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.spinCube)
        self.timer.Start()

    
    def OnPaint (self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.initGL()
        self.clear()
        self.setProjection()
        self.setViewpoint()
        self.drawWorld()
        self.SwapBuffers()
    
    def OnSize (self, event):
        self.width, self.height = self.GetSizeTuple()
    
    def initGL (self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND);
        glEnable(GL_DEPTH_TEST)
        self.init = True
    
    def clear (self):
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    def setProjection (self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(self.width) / float(self.height), Near, Far)
        glMatrixMode(GL_MODELVIEW)
    
    def setViewpoint (self):
        glLoadIdentity()
        gluLookAt(-5, 2.0, 5.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)
    
    def drawWorld (self):
        glPushMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glRotatef(-1*self.spin,0,1,0)
        drawCube(self.s1,self.s2,self.s3,self.s4,self.s5,self.s6,self.s7,
                 self.s8,self.s9)
        glPopMatrix()
    
    def spinCube (self, event):
        global beats
        global onset
        global path
        global notes
        
        self.spin = (self.spin + 1) % 360
        
        if len(beats) > 0:
            if self.setStart == False:
                self.startTime = int(round(time.time() * 1000))
                self.setStart = True
            currentTime = int(round(time.time() * 1000)) - self.startTime   

            if self.startAudio == False:
                self.sound = wx.Sound(path)
                if self.sound.IsOk():
                    self.sound.Play(wx.SOUND_ASYNC)
                self.startAudio = True

            if self.tick < len(beats) - 1:
                if round(float(currentTime)/1000,2) == beats[self.tick] or \
                (round(float(currentTime)/1000,2) > beats[self.tick] and \
                 round(float(currentTime)/1000,2) < beats[self.tick+1]):
                    self.s1 = 6
                    self.tick = self.tick + 1

            if round(float(currentTime)/1000,2) in onset:
                i = onset.index(round(float(currentTime)/1000,2))
                x = notes[i]
                if x >= 21 and x < 55:
                    self.s7 = 3
                    if self.s3 < .5:
                        self.s3 = .5
                    if self.s4 < .5:
                        self.s4 = .5
                if x >= 55 and x < 60:
                    self.s3 = 3
                    if self.s7 < .5:
                        self.s7 = .5
                    if self.s9 < .5:
                        self.s9 = .5
                if x >= 60 and x < 68:
                    self.s9 = 3
                    if self.s3 < .5:
                        self.s3 = .5
                    if self.s5 < .5:
                        self.s5 = .5
                if x >= 68 and x < 74:
                    self.s5 = 3
                    if self.s9 < .5:
                        self.s9 = .5
                    if self.s8 < .5:
                        self.s8 = .5
                if x >= 74 and x < 80:
                    self.s8 = 3
                    if self.s5 < .5:
                        self.s5 = .5
                    if self.s2 < .5:
                        self.s2 = .5
                if x >= 80 and x < 88:
                    self.s2 = 3
                    if self.s8 < .5:
                        self.s8 = .5
                    if self.s6 < .5:
                        self.s6 = .5
                if x >= 87 and x < 96:
                    self.s6 = 3
                    if self.s2 < .5:
                        self.s2 = .5
                    if self.s4 < .5:
                        self.s4 = .5
                if x > 96 and x < 120:
                    self.s4 = 3
                    if self.s7 < .5:
                        self.s7 = .5
                    if self.s6 < .5:
                        self.s6 = .5
                    
        if self.s1 > 0:
            self.s1 -= .1
        if self.s2 > 0:
            self.s2 -= .1
        if self.s3 > 0:
            self.s3 -= .1
        if self.s4 > 0:
            self.s4 -= .1
        if self.s5 > 0:
            self.s5 -= .1
        if self.s6 > 0:
            self.s6 -= .1
        if self.s7 > 0:
            self.s7 -= .1
        if self.s8 > 0:
            self.s8 -= .1
        if self.s9 > 0:
            self.s9 -= .1
        
        self.Refresh(eraseBackground=False)

class Gui(wx.App):
    def OnInit(self):
        self.myframe = GuiFrame(None, -1, "PyDSP")
        self.canvas = myGLCanvas(self.myframe)
        self.myframe.CenterOnScreen()
        self.myframe.Show(True)
        return True