#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 11:02:11 2022

@author: Killshot
"""
# %% imports
import matplotlib.pyplot as plt
import csv
import numpy as np
# %% pre-INIT
from matplotlib.pyplot import close

# close all figures
close('all')
# %% file name spec
FILEPATH = '../data/'
FILENAME = 'test_data.csv'


# %% Function definitions
def read_movement_data():
    movement = []
    with open(FILEPATH + FILENAME, 'r',
              encoding='unicode_escape') as csvFile:  # unicode escape as a failsafe in case of any non utf-8 chars
        movement_data = csv.reader(csvFile, delimiter=',')

        for row in movement_data:
            if row[0] == 'frame':  # done to ignore comments and other entries at start
                movement.append(row)

        return movement


def update_visualization(val):
    # user def <- sadly had to do this that way since update fun can only accept single float callable
    # (at least according to documentation)
    marker_to_follow = 5  # in data samples used for development of this script the chest was
    # marker 5 hence the pick arbitrary pick here
    height = 2.2  # should be changed if your markers go over 2.2 m or near that value
    offset = 1.5  # how far we look in x and y aka distance from center point of visualization*
    # *defined by distance norm of norm = |x + y| aka square
    follow_marker = False  # if one for stalking
    # fun
    frame_to_display = int(slider.val)
    ax.cla()  # aka clean
    markers_x = visualization[frame_to_display][:, 0]
    markers_y = visualization[frame_to_display][:, 2]  # we remember to reverse y-axis with z for proper
    # (at least for humans) orientation of the visualization
    markers_z = visualization[frame_to_display][:, 1]
    ax.scatter(markers_x, markers_y, markers_z, 'red', marker='.')
    # defining the limits
    if follow_marker:
        ax.set_xlim(markers_x[marker_to_follow] - offset, markers_x[marker_to_follow] + offset)
        ax.set_ylim(markers_y[marker_to_follow] - offset, markers_y[marker_to_follow] + offset)
    else:
        ax.set_xlim(-offset, offset)
        ax.set_ylim(-offset, offset)
    ax.set_zlim(0, height)
    ax.axis('off')


# %% import data
data = read_movement_data()
number_of_frames = len(data)
markers_start_after_col = 5  # 5 but we count from 0
markers_info_col = 4  # columni in which we have info about number of collected markers
entries_per_marker = 5  # number of row entries per marker, in example data case [x, y, z, markerId, markerName]
# %% Process data
visualization = []
# creating processed dataset for visualization purposes
for frame in range(0, number_of_frames):
    markers = []
    for marker in range(int(data[frame][markers_info_col])):
        x = (float(data[frame][markers_start_after_col + entries_per_marker * marker + 0]))
        y = (float(data[frame][markers_start_after_col + entries_per_marker * marker + 1]))
        z = (float(data[frame][markers_start_after_col + entries_per_marker * marker + 2]))
        markers.append([x, y, z])
    visualization.append(np.array(markers))

# %% VISUALIZATION: All i see is dots
plt.close(1)
fig = plt.figure(1)
fig.suptitle('~|mo-cap marker recording visualization by frame|~\n*click here to interact with slider*:')
ax = fig.add_axes([0, 0, 1, 0.9], projection='3d')  # one for a plot
axSlider = fig.add_axes([0.1, 0.9, 0.8, 0.1])  # one for a 'suwaczek gui'

slider = plt.Slider(axSlider, 'frame', valmin=0, valmax=(number_of_frames - 1), valinit=1,
                    valfmt='%0.0f')  # valfmt since we only want integers

slider.on_changed(update_visualization)
update_visualization(0)  # initial plot <- cal for update function in frame 0
fig.show()
