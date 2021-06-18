# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:06:28 2021

@author: Joao
"""
import ffmpeg
import numpy as np
from scipy.io import wavfile
import utils
import pandas as pd

TIME_PER_FRAME = 0.25
sustain_level  = 0.1

data_list   = np.load('data.npy')
notes_order = ['C', 'D', 'E', 'F', 'G', 'A', 'B']


right_hand_notes    = []
right_hand_duration = []

left_hand_notes    = []
left_hand_duration = []

for df in data_list:

    data = pd.DataFrame(df)

    data.index   = ['3']*25 + ['4']*25
    data.columns = ['C']*6 + ['D']*6 + ['E']*6 + ['F']*6 + ['G']*6 + ['A']*6 + ['B']*4
    
    
    
    
    right_data = data.iloc[:25, :].copy()
    left_data  = data.iloc[25:, :].copy()
    
    right_notes = {}
    left_notes  = {}
    
    right_temp = {'C': right_data['C'].max().sum(), 'D': right_data['D'].max().sum(), 'E': right_data['E'].max().sum(), 
                  'F': right_data['F'].max().sum(), 'G': right_data['G'].max().sum(), 'A': right_data['A'].max().sum(), 
                  'B': right_data['B'].max().sum()}
    
    compare = 0
    for note in notes_order:
        if right_temp[note] > compare:
            compare = right_temp[note]
            right_notes[1] = note
            
    right_hand_duration.append(TIME_PER_FRAME/2)
    right_hand_notes.append(right_notes[1] + str(4))
    '''
    compare = [0, 0]
    for note in notes_order:
        if right_temp[note] > compare[0]:
            
            if len(right_notes) != 0:    
                compare[1]     = compare[0]
                right_notes[2] = right_notes[1]
                
            right_notes[1] = note
            compare[0]     = right_temp[note]
            
        else:
            
            if right_temp[note] > compare[1]:
                right_notes[2] = note
                compare[1]     = right_temp[note]
        
    right_hand_duration.append(TIME_PER_FRAME*(right_temp[right_notes[1]])/(right_temp[right_notes[1]] + right_temp[right_notes[2]]))
    right_hand_duration.append(TIME_PER_FRAME - TIME_PER_FRAME*(right_temp[right_notes[1]])/(right_temp[right_notes[1]] + right_temp[right_notes[2]]))
    
    right_hand_notes.append(right_notes[1] + str(4))
    right_hand_notes.append(right_notes[2] + str(4))
    '''
    left_temp = {'C': left_data['C'].max().sum(), 'D': left_data['D'].max().sum(), 'E': left_data['E'].max().sum(), 
                 'F': left_data['F'].max().sum(), 'G': left_data['G'].max().sum(), 'A': left_data['A'].max().sum(), 
                 'B': left_data['B'].max().sum()}
    compare = 0
    for note in notes_order:
        if left_temp[note] > compare:
            compare = left_temp[note]
            left_notes[1] = note
            
    left_hand_duration.append(TIME_PER_FRAME/2)
    left_hand_notes.append(left_notes[1] + str(4))
    '''
    compare = [0, 0]
    for note in notes_order:
        if left_temp[note] > compare[0]:
           
            if len(left_notes) != 0:
            
                compare[1]    = compare[0]
                left_notes[2] = left_notes[1]
            
            left_notes[1] = note
            compare[0]    = left_temp[note] 
            
        else:
            
            if left_temp[note] > compare[1]:
                left_notes[2] = note
                compare[1]    = left_temp[note]
    
    left_hand_duration.append(TIME_PER_FRAME*(left_temp[left_notes[1]])/(left_temp[left_notes[1]] + left_temp[left_notes[2]]))
    left_hand_duration.append(TIME_PER_FRAME - TIME_PER_FRAME*(left_temp[left_notes[1]])/(left_temp[left_notes[1]] + left_temp[left_notes[2]]))
    
    left_hand_notes.append(left_notes[1] + str(4))
    left_hand_notes.append(left_notes[2] + str(4))
    '''
    
# %%

factor     = [0.68, 0.26, 0.03, 0.03]
length     = [0.01, 0.6, 0.29, 0.1]
decay      = [0.05, 0.02, 0.005, 0.1]
right_hand = utils.get_song_data(right_hand_notes, right_hand_duration, TIME_PER_FRAME,
                                 factor, length, decay, sustain_level)

factor    = [0.68, 0.26, 0.03, 0.03]
length    = [0.01, 0.6, 0.29, 0.1]
decay     = [0.05, 0.02, 0.005, 0.1]
left_hand = utils.get_song_data(left_hand_notes, left_hand_duration, TIME_PER_FRAME,
                                 factor, length, decay, sustain_level)

data = left_hand + right_hand
data = data * (4096/np.max(data))
wavfile.write('test.wav', 44100, data.astype(np.int16))

# %%
video = ffmpeg.input('C:/Users/Joao/Work/OPERATION/CFS_GIF/precipitation_rate.mp4')
audio = ffmpeg.input('C:/Users/Joao/Desktop/test.mp4')

stream = ffmpeg.output(video, audio, 'C:Users/Joao/Desktop/final.mp4').run()
