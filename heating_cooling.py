# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 17:54:26 2022

@author: Hina
"""

import numpy as np
import matplotlib.pyplot as plt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Author: Hina Goto, 2022 summer CRESST II/NASA GSFC code 662 intern          #
# Date: 08/12/2022                                                            #
# Contact: hina0830@email.arizona.edu                                         #
# Description: This program deals with the output files of the                #
#              save heating/cooling command in Cloudy. It reads the files,    #
#              creates a dictionary of elements and the corresponding         #
#              fractions as well as the total heating/cooling rates.          #
#              Lastly, it plots total heating/cooling rates vs density        #
#              and fractional heating/cooling rates  vs  density              #
#              for all elements at xi of your choice                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


def param_to_grid(xi_lin, hden_lin, grid):
    """
    This function creates a dictionary that converts
    a pair of xi and density to grid number

    Inputs are following 3 arrays: xi_lin (array of xi used in simulation),
    hden_lin (array of hden used in simulation), and grids (array of grids
    Cloudy produces)

    grid_dict[xi][n] tells you the grid at given xi and n
    """
    grid_dict = {}
    i = 0
    for xi in xi_lin:
        grid_dict[xi] = {}
        for n in hden_lin:
            grid_dict[xi][n] = grid[i]
            i += 1
    return grid_dict


def read_file(path, filename, index):
    """
    **** For heating, give index == 0 ****
    **** For cooling, give index == 1 ****

    This function reads the output file "save heating/save cloudy"
    command produces and retuns an array of first rows at grid
    """

    # Read the appropriate output file
    if index == 0:  # HEATING
        file = open(path + "/" + filename + "_heat.txt")
    elif index == 1:  # COOLING
        file = open(path + "/" + filename + "_cool.txt")

    # Reads the file line by line and column by column
    file.readline()
    raw_data = []
    fraction = []
    for line in file:
        line = line.rstrip("\n")
        line = line.split("\t")
        raw_data.append(line)

    if index == 0:  # HEATING
        initial_arr = raw_data[0][2:]  # column Htot to the end
        fraction.append(initial_arr)
        for i in range(len(raw_data) - 1):
            if len(raw_data[i]) == 1 and len(raw_data[i + 1][2:-1]) > 0:
                fraction.append(
                    raw_data[i + 1][2:]
                )  # row right after the grid row == first row of the next grid

    elif index == 1:  # COOLING
        initial_arr = raw_data[0][3:]  # column Ctot to the end
        fraction.append(initial_arr)
        for i in range(len(raw_data) - 1):
            if (
                len(raw_data[i]) == 1 and len(raw_data[i + 1][2:-1]) > 0
            ):  # if ['########################### GRID_DELIMIT -- grid000000000'] is found
                fraction.append(
                    raw_data[i + 1][3:]
                )  # saves the row right after the grid row == first row of the next grid
    return fraction


def convert(xi, n, fraction, grid_dict, index):
    """
    **** For heating, give index == 0 ****
    **** For cooling, give index == 1 ****

    This function used the array from read_file(path, filename, index)
    to produce a dicionary of element and its fraction at a pair of xi and n
    """

    grid = int(grid_dict[xi][n])
    thisdict = {}
    for i in range(len(fraction)):  # == grid number
        # thisdict = {}
        if index == 0:  # HEATING
            if i == int(grid):
                # print(i)
                for j in range(0, len(fraction[i]) - 1, 2):
                    if j == 0:
                        thisdict["total"] = float(fraction[i][j])
                    elif j == 1:
                        pass
                    else:
                        thisdict[fraction[i][j]] = float(
                            fraction[i][j + 1].rstrip("\n")
                        )
        if index == 1:  # COOLING
            if i == int(grid):
                for j in range(0, len(fraction[i]), 2):
                    if j == 0:
                        thisdict["total"] = float(fraction[i][j])
                    else:
                        thisdict[fraction[i][j - 1][:-4]] = float(
                            fraction[i][j].rstrip("\n")
                        )
    return thisdict


def dictionary_final(fraction_heat, grid_dict, xi_lin, hden_lin, index):
    """
    **** For heating, give index == 0 ****
    **** For cooling, give index == 1 ****

    This function produces a multidimensional dictionary that gives you
    the elements and corresponding fractions at all xi and n.

    To access the elements and fractions (and total) at any xi and n,
    use dict_final[xi][n]
    """

    dict_final = {}
    for xi in xi_lin:
        dict_final[xi] = {}
        for n in hden_lin:
            final = convert(xi, n, fraction_heat, grid_dict, index)
            dict_final[xi][n] = final
    return dict_final


def elements(dict_final, xi_lin, hden_lin):
    """
    This function uses dict_final to create a set of elements
    that appear in the simulations. It will be used to label
    the data points when creating plots
    """

    element_set = set([])
    for xi in xi_lin:
        for n in hden_lin:
            element_set = element_set.union(set(dict_final[xi][n].keys()))
    element_set.remove("total")
    return element_set


def total_vs_n(xi, hden_lin, element_set, dict_final, index):
    """
    **** For heating, give index == 0 ****
    **** For cooling, give index == 1 ****

    This function creates a plot of total heating/cooling vs density
    """

    fig, ax = plt.subplots(figsize=(10, 9))
    if index == 0:  # HEATING
        ax.set_title("Heating total vs density log($\\xi$)=" + str(xi), fontsize=18)
        plt.ylabel("Heating total", fontsize=18)
    elif index == 1:  # COOLING
        ax.set_title("Cooling total vs density log($\\xi$)=" + str(xi), fontsize=18)
        plt.ylabel("Heating total", fontsize=18)
    plt.xlabel(r"log(n$_H$/[cm$^{-3}$])", fontsize=18)
    ax.tick_params(axis="x", labelsize=18)
    ax.tick_params(axis="y", labelsize=18)

    colors = plt.cm.rainbow(np.linspace(0, 1, len(element_set)))
    i = 0
    for element in element_set:
        y = np.array([])
        x = np.array([])
        for n in hden_lin:
            if element in dict_final[xi][n]:
                y = np.append(
                    y, dict_final[xi][n][element] * dict_final[xi][n]["total"]
                )
                x = np.append(x, n)
        plt.plot(x, y, label=element, color=colors[i])
        i += 1
    plt.legend()
    return ax


def frac_vs_n(xi, hden_lin, element_set, dict_final, index):
    """
    **** For heating, give index == 0 ****
    **** For cooling, give index == 1 ****

    This function creates a plot of heating/cooling fraction vs density
    """

    fig, ax = plt.subplots(figsize=(10, 9))
    if index == 0:  # HEATING
        ax.set_title("Heating fraction vs density log($\\xi$)=" + str(xi), fontsize=18)
        plt.ylabel("Heating fraction", fontsize=18)
    elif index == 1:  # COOLING
        ax.set_title("Cooling fraction vs density log($\\xi$)=" + str(xi), fontsize=18)
        plt.ylabel("Cooling fraction", fontsize=18)
    plt.xlabel(r"log(n$_H$/[cm$^{-3}$])", fontsize=18)
    ax.tick_params(axis="x", labelsize=18)
    ax.tick_params(axis="y", labelsize=18)

    colors = plt.cm.rainbow(np.linspace(0, 1, len(element_set)))
    i = 0
    for element in element_set:
        a = np.array([])
        b = np.array([])
        for n in hden_lin:
            if element in dict_final[xi][n]:
                a = np.append(a, dict_final[xi][n][element])
                b = np.append(b, n)
        plt.plot(b, a, label=element, color=colors[i])
        i += 1
    plt.legend()
    return ax
