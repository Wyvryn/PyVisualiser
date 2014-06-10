'''
@author: Mike
'''
import wave
import numpy as np
import sys
import subprocess
import math

class Process(object):
    '''
    Takes in file name and returns the waveform as a plottable string
    '''

    def __init__(self):
        self.Time = 0
        self.signal = 0
        self.frameRate = 0
        self.bpm = 0
        self.beats = []
        self.onset = []
        self.fft = []
        self.notes = []
        
    def procWav(self, fileName):
        waveForm = wave.open(fileName, 'r')
        self.frameRate = waveForm.getframerate()
        frames=waveForm.getnframes()
        duration=frames/float(self.frameRate)

        signal = waveForm.readframes(-1)
        self.signal = np.fromstring(signal, 'Int16')
        self.signal = self.signal[::self.frameRate/100]
        
        
        w = np.fft.fft(self.signal)
        self.fft = w
        frq = np.fft.fftfreq(len(self.fft), self.frameRate)
        
    
                    
        if waveForm.getnchannels() == 2:
            print "Mono Files only (For now)"
            sys.exit(0)
            
        cmd = "aubiotrack.exe -i "+fileName
        beats = subprocess.check_output(cmd,shell=False)
        beats = beats.split()
        
        self.beats = [round(float(i),2) for i in beats]
        
        self.bpm = len(beats) * 4 * duration / 60
        
        cmd = "aubionotes.exe -i "+fileName
        notes = subprocess.check_output(cmd,shell=False)
        notes = notes.split()


        for i in range(len(notes)-1):
            if float(notes[i])%1 == 0:
                self.notes.append(float(notes[i]))
                self.onset.append(float(notes[i+1]))
            
        self.onset = [round(float(i),2) for i in self.onset]
