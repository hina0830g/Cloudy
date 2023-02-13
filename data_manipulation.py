# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 17:00:22 2022

@author: Hina
"""
import numpy as np

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Author: Hina Goto, 2022 summer CRESST II/NASA GSFC code 662 intern          #
# Date: 07/07/2022                                                            #
# Contact: hina0830@arizona.edu                                               #
# Description: This program deals with the output files                       #
#              of the spectral simnulation software Cloudy.                   #
#              It extract necessary information in the files and save         #
#              the values as arrays for easier manipulation of the data.      #
#                                                                             #
#              This was written for the Cloudy simulations where grid         #
#              command was used for ionization parameter xi and               #
#              hdrogen dennsity hden                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #               


# ----------------- Description of logspace ------------------ #
# logspace takes initial, final value, and the stepsize        #
# used in Cloudy simulation and creates appropriate arrays;    #
#                                                              #
# For example, do xi = logspace(-1, 6, 1) if the grid command  #
# you defined looks like the following:                        #
#  xi 0 vary grid -1 to 6 dex 1 ncpus 4                        #
# -------------------- End of Description -------------------- #

def logspace(start, stop, step=1.0):
    """
    Like np.logspace but uses step instead of num
    This is inclusive to stop, so if start=1, stop=3, step=0.5
    Output is: 10**(array([1., 1.5, 2., 2.5, 3.]))

    Use this to create arrays of hydrogen number density and
    ionization parameter xi.
    """
    return np.logspace(start, stop, int((stop - start) / step + 1))


def linspace(start, stop, step=1.0):
    return np.linspace(start, stop, int((stop - start) / step + 1))


# ----------------- Description of temp_txt ------------------ #
# temp_txt takes path and the prefix of the tempeature file    #
# (= name w/o the file extension such as .txt), which can be   #
# obtained as one of the out files in Cloudy.                  #                                                           #
# This function extracts the values of temperatures and depth  #
# and save them as arrays. They will have the same dimension   #
# therefore can be used to create a plot temperature vs depth. #
#                                                              #
# When calling the function, define two arrays. For example,   #
# depth_arr, Te_arr = temp_txt(home/cloudy, sed1)              #
# -------------------- End of Description -------------------- #

def temp_txt(path, prefix):
    """Reads the _temp.txt file and
    extract (return) the temperatures and depth
    """
    depth, Te = np.array([]), np.array([])
    grid = 0
    file = open(path + "/" + prefix + "_temp.txt")
    file.readline()
    for line in file:
        line = line.rstrip("\n")
        line = line.split("\t")
        try:
            depth = np.append(depth, float(line[0]))
            Te = np.append(Te, float(line[1]))
        except:
            depth = np.append(depth, str(line))
            Te = np.append(Te, str(line))
            grid += 1

    listOfLists_depth = [[] for i in range(grid)]
    listOfLists_Te = [[] for i in range(grid)]

    index = 0
    for i in range(len(depth)):
        try:
            listOfLists_depth[index].append(float(depth[i]))
            listOfLists_Te[index].append(float(Te[i]))
        except ValueError:
            index += 1

    return listOfLists_depth, listOfLists_Te


def avg_temp_txt(path, prefix, xi):
    xi_len = len(xi)
    file = open(path + "/" + prefix + "_temp_avg.txt")
    file.readline()
    avg_temp = np.array([])
    for line in file:
        line = line.rstrip("\n")
        line = line.split("\t")
        try:
            avg_temp = np.append(avg_temp, float(line[1]))
        except IndexError:  # Skips the raws of strings (=grids)
            pass
    avg_temp_split = np.array_split(list(avg_temp), xi_len)

    return avg_temp_split


def temp_ratio(hden, avg_temp_split):
    n_transition, te_transition = np.array([]), np.array([])
    for index in range(len(avg_temp_split)):
        #i = 0
       # while True:
           for i in range(0, len(avg_temp_split[0])-1):
           # i += 1
            if avg_temp_split[index][i + 1] / avg_temp_split[index][i] >= 1.01:
                n_transition = np.append(n_transition, hden[i])
                te_transition = np.append(te_transition, avg_temp_split[index][i])
                break
    return n_transition, te_transition


def temp_max(listOfLists_Te, xi):
    xi_len = len(xi)
    listOfLists_max = np.array([])
    for i in listOfLists_Te:
        listOfLists_max = np.append(listOfLists_max, np.max(i))
    temp_max_split = np.array_split(list(listOfLists_max), xi_len)
    return temp_max_split


def avg_temp_2d(hden, avg_temp_split):
    avg_temp_2darr = []
    for j in range(len(hden)):
        a = [i[j] for i in avg_temp_split]
        avg_temp_2darr.append(a)
    return avg_temp_2darr
