#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 11:02:11 2022

@author: Killshot
"""
#%% imports
import matplotlib.pyplot as plt
import csv
import numpy as np
#%% pre-INIT
from matplotlib.pyplot import close
# close all figures
close('all')
#%% filespec
FILEPATH = 'MotionGains_data/1/'
FILENAME = 'Patryk_1.csv'
# FILENAME = 'Pawel_2.csv'
# FILENAME = 'natalia_1.csv'
# FILENAME = 'kamil-robi-cos.csv'
#%% Function defs
def readMovementData():
    movement = []
    with open(FILEPATH + FILENAME, 'r', encoding='unicode_escape') as csvFile: # unicode escape as a failsave in case of any non utf-8 chars
        movementData = csv.reader(csvFile, delimiter = ',')
        
        for row in movementData:
            if row[0] == 'frame': # done to ignore comments and other entries at start
                movement.append(row)
            
        return movement
    
def updateVisuzalization(val):
    # user def <- sadly had to do this that way since update fun can only accept single float callable (according to documentation)
    marker_to_follow = 5    # in collected data samples used for development of this script the chest was marker 5 hence the pick here
    height = 2.2            # should be changed if your markers go over 2.2 m or near that value
    offset = 1.5            # how far we look in x and y aka distance from center point of visualization defined by distance norm of norm = |x + y|
    follow_marker = False   # if one for stalking?
    # fun
    frame = int(slider.val)
    ax.cla() # aka clean
    x = visualization[frame][:,0]
    y = visualization[frame][:,2]     # we remember to reverse y axis with z for proper (at least for humans) orientation of the visualization
    z = visualization[frame][:,1]
    ax.scatter(x, y, z, 'red', marker='.')
    # defining the limits
    if follow_marker:
        ax.set_xlim(x[marker_to_follow] - offset, x[marker_to_follow] + offset)  # Limits chosen arbitrarly to make the scale somewhat resemble the real human
        ax.set_ylim(y[marker_to_follow] - offset, y[marker_to_follow] + offset)  # ^
    else:
        ax.set_xlim(-offset, offset)  # Limits chosen arbitrarly to make the scale somewhat resemble the real human
        ax.set_ylim(-offset, offset)  # ^
    ax.set_zlim(0, height) 
    
#%% import data
data = readMovementData()
number_of_frames = len(data)
markers_start_after_col = 5 # 5 but we count from 0
markers_info_col = 4 # columni in which we have info about number of collected markers
entries_per_marker = 5 # number of row entries per marker, in example data case [x, y, z, markerId, markerName]
#%% Process data
visualization = []
# creating processed dataset for visualization purposes
for frame in range(0, number_of_frames):    
    markers = []
    for marker in range(int(data[frame][markers_info_col])): 
        x = (float(data[frame][markers_start_after_col + entries_per_marker*marker + 0]))
        y = (float(data[frame][markers_start_after_col + entries_per_marker*marker + 1]))
        z = (float(data[frame][markers_start_after_col + entries_per_marker*marker + 2]))
        markers.append([x, y, z])
    visualization.append(np.array(markers))
 
#%% VISUALIZATION: All i see is dots   
plt.close(1) 
fig = plt.figure(1)
fig.suptitle('~|mocap marker recording visualization by frame|~\n*click here to interact with slider*:')
ax = fig.add_axes([0, 0, 1, 0.9], projection= '3d') # one for a plot
axSlider = fig.add_axes([0.1, 0.9, 0.8, 0.1]) # one for a 'suwaczek gui'

slider = plt.Slider(axSlider, 'frame', valmin=0, valmax=(number_of_frames - 1), valinit=1, valfmt='%0.0f') # valfmt since we only want integers
 
slider.on_changed(updateVisuzalization)
updateVisuzalization(0) # initial plot <- cal for update function in frame 0
fig.show()