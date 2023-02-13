# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 18:40:02 2022

@author: Hina
"""

import numpy as np
import matplotlib.pyplot as plt

# Author: Hina Goto, 2022 summer CRESST II/NASA GSFC code 662 intern
# Date: 07/12/2022
# Contact: hina0830@arizona.edu
# General description: This is a modified version of results_plot.py
# for when using finer grids and only showing the specific data points
# (such as when log(xi) = integers)


def nTransition_vs_xi(xi, n_transition, n_transition2, n_transition3, prefix):
    fig, ax = plt.subplots(figsize=(10, 9))
    plt.title(
        "entering point to the high density regime (" + str(prefix) + ")", fontsize=14
    )
    plt.xlabel("ionization number $\chi$", fontsize=14)
    plt.ylabel("number density $n_h$ [$cm^{-3}$]", fontsize=14)
    plt.xscale("log")
    plt.yscale("log")
    plt.plot(xi, n_transition, marker="*", markersize=10, label="all")
    plt.plot(xi, n_transition2, marker="o", markersize=10, label="intermediate")
    plt.plot(xi, n_transition3, marker="^", markersize=10, label="no IR")
    plt.legend()
    return ax


### Leaves notes below:
### avg_temp_split_stacked[i][0] -> avg_temp_split for first input
### avg_temp_split_stacked[i][1] -> avg_temp_split for second input
### avg_temp_split_stacked[i][2] -> avg_temp_split for third input


def AvgTemp_vs_n(
    hden,
    xi,
    xi_lin,
    avg_temp_split_stacked,
    n_transition_stacked,
    Te_transition_stacked,
    name_index,
):
    fig, ax = plt.subplots(figsize=(10, 9))
    plt.title("Average temperature vs number density of Mrk509", fontsize=15)
    plt.xlabel(r'log($\frac{n_{H}}{cm^{-3}}$)', fontsize=15)
    plt.ylabel(r'log(${10}$T/[K]', fontsize=15)
    #plt.xscale("log")
    #plt.yscale("log")

    colors = plt.cm.rainbow(np.linspace(0, 1, len(avg_temp_split_stacked)))
    xi_stepsize = np.abs(xi_lin[0] - xi_lin[1])
    increment = int(1 / xi_stepsize)
    i = 0
    while i <= (len(xi)): # - increment):
        row = avg_temp_split_stacked[i][0]
        #row = np.log10(avg_temp_split_stacked[i][0])
        (index,) = np.where(row != 1e-30)

        if len(index) == len(row):
            plt.plot(
                hden, np.log10(row), color=colors[i]
            )  # , label= 'xi='  + str(i-1) + ' (' + str(name_index[0]) + ')')
        else:
            (i_1e30,) = np.where(row == 1e-30)
            end = i_1e30[0]
            plt.plot(
                hden[index], np.log10(row)[0:end], color=colors[i]
            )  # , label= 'xi=' + str(i-1) + ' (' + str(name_index[0]) + ')')

        row_med = avg_temp_split_stacked[i][1]
        #row_med = np.log10(avg_temp_split_stacked[i][1])
        (index_med,) = np.where(row_med != 1e-30)
        if len(index_med) == len(row_med):
            plt.plot(
                hden, np.log10(row_med), color=colors[i], linestyle=":"
            )  # , label= 'xi='  + str(i-1) + ' (' + str(name_index[1]) + ')')
        else:
            (i_1e30_med,) = np.where(row_med == 1e-30)
            end_med = i_1e30_med[0]
            plt.plot(
                hden[index_med], np.log10(row_med)[0:end_med], color=colors[i], linestyle=":"
            )  # , label= 'xi=' + str(i-1) + ' (' + str(name_index[1]) + ')')

        row_noIR = np.array(avg_temp_split_stacked[i][2])
        #row_noIR = np.log10(np.array(avg_temp_split_stacked[i][2]))
        (index_noIR,) = np.where(row_noIR != 1e-30)
        if len(index_noIR) == len(row_noIR):
            plt.plot(
                hden, np.log10(row_noIR), color=colors[i], linestyle="--"
            )  # , label= 'xi='  + str(i-1) + ' (' + str(name_index[2]) + ')'
            plt.text(hden[0], np.log10(row_noIR)[0], "xi=" + str(xi_lin[i]), fontsize=12)
        else:
            (i_1e30_noIR,) = np.where(row_noIR == 1e-30)
            end_noIR = i_1e30_noIR[0]
            plt.plot(
                hden[index_noIR], np.log10(row_noIR)[0:end_noIR], linestyle="--"
            )  # , color=colors[i], label= 'xi=' + str(i-1) + ' (' + str(name_index[0]) + ')')
            plt.text(hden[0], np.log10(row_noIR)[0], "xi=" + str(xi_lin[i]), fontsize=12)
        plt.scatter(
            n_transition_stacked[0][i],
            np.log10(Te_transition_stacked[0][i]),
            color=colors[i],
            marker="*",
            s=160,
        )  # , label='all')
        plt.scatter(
            n_transition_stacked[1][i],
            np.log10(Te_transition_stacked[1][i]),
            color=colors[i],
            marker="o",
            s=100,
        )  # , label='med')
        plt.scatter(
            n_transition_stacked[2][i],
            np.log10(Te_transition_stacked[2][i]),
            color=colors[i],
            marker="^",
            s=100,
        )  # , label='no IR')
        i += increment

    plt.scatter(
        n_transition_stacked[0][0],
        np.log10(Te_transition_stacked[0][0]),
        color=colors[0],
        marker="*",
        s=160,
        label=" (" + str(name_index[0]) + ")",
    )
    plt.scatter(
        n_transition_stacked[1][0],
        np.log10(Te_transition_stacked[1][0]),
        color=colors[0],
        marker="o",
        s=100,
        label=" (" + str(name_index[1]) + ")",
    )
    plt.scatter(
        n_transition_stacked[2][0],
        np.log10(Te_transition_stacked[2][0]),
        color=colors[0],
        marker="^",
        s=100,
        label=" (" + str(name_index[2]) + ")",
    )

    plt.plot(
        hden,
        np.log10(avg_temp_split_stacked[0][0]),
        color=colors[0],
        label=" (" + str(name_index[0]) + ")",
    )
    plt.plot(
        hden,
        np.log10(avg_temp_split_stacked[0][1]),
        color=colors[0],
        label=" (" + str(name_index[1]) + ")",
        linestyle=':',
    )
    plt.plot(
        hden,
        np.log10(avg_temp_split_stacked[0][2]),
        color=colors[0],
        label=" (" + str(name_index[2]) + ")",
        linestyle='--'
    )

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    return ax


def AvgTemp_vs_n_1(
    hden,
    xi,
    xi_lin,
    avg_temp_split_stacked,
    n_transition_stacked,
    Te_transition_stacked,
    name_index,
):
    fig, ax = plt.subplots(figsize=(10, 9))
    plt.title("Average temperature vs number density of Mrk509", fontsize=15)
   #plt.xlabel(r'log($\frac{n_{H}}{cm^{-3}}$)', fontsize=15)
    plt.xlabel(r'log$_{10}$(n$_H$/[cm$^{-3}$])', fontsize=15)
    plt.ylabel(r'log$_{10}$(T/[K])', fontsize=15)
    #plt.xscale("log")
    #plt.yscale("log")

    colors = plt.cm.rainbow(np.linspace(0, 1, len(avg_temp_split_stacked)))
    xi_stepsize = np.abs(xi_lin[0] - xi_lin[1])
    increment = int(1 / xi_stepsize)
    i = 0
    while i <= (len(xi)): # - increment):
        row = avg_temp_split_stacked[i][0]
        #row = np.log10(avg_temp_split_stacked[i][0])
        (index,) = np.where(row != 1e-30)

        if len(index) == len(row):
            plt.plot(
                hden, np.log10(row), color=colors[i]
            )  # , label= 'xi='  + str(i-1) + ' (' + str(name_index[0]) + ')')
        else:
            (i_1e30,) = np.where(row == 1e-30)
            end = i_1e30[0]
            plt.plot(
                hden[index], np.log10(row)[0:end], color=colors[i]
            )  # , label= 'xi=' + str(i-1) + ' (' + str(name_index[0]) + ')')

        plt.scatter(
            n_transition_stacked[0][i],
            np.log10(Te_transition_stacked[0][i]),
            color=colors[i],
            marker="*",
            s=160,
        )  # , label='all')
        i += increment

    plt.scatter(
        n_transition_stacked[0][0],
        np.log10(Te_transition_stacked[0][0]),
        color=colors[0],
        marker="*",
        s=160,
        label=" (" + str(name_index[0]) + ")",
    )

    plt.plot(
        hden,
        np.log10(avg_temp_split_stacked[0][0]),
        color=colors[0],
        label=" (" + str(name_index[0]) + ")",
    )

    plt.text(hden[0], np.log10(avg_temp_split_stacked[0][0][0]), "xi=" + str(xi_lin[0]), fontsize=12)
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    return ax

def TempRatio_vs_n(
    hden,
    xi,
    xi_lin,
    avg_temp_split,
    avg_temp_split_med,
    avg_temp_split_noIR,
    name_index,
):
    T_ratio = np.exp(np.diff(np.log(avg_temp_split)))
    T_ratio_med = np.exp(np.diff(np.log(avg_temp_split_med)))
    T_ratio_noIR = np.exp(np.diff(np.log(avg_temp_split_noIR)))
    hden_ratio = (hden[1:] + hden[:-1]) / 2

    fig, ax = plt.subplots(figsize=(10, 9))
    plt.title("Ratio of temperature vs number density", fontsize=14)
    plt.xlabel("number density $n_h$ [$cm^{-3}$]", fontsize=13)
    plt.ylabel("Ratio (T[i+1] / T[i])", fontsize=13)
    plt.xscale("log")
    plt.ylim(0.9, 1.2)
    # plt.yscale('log')
    colors = plt.cm.rainbow(np.linspace(0, 1, len(T_ratio)))
    xi_stepsize = np.abs(xi_lin[0] - xi_lin[1])
    increment = int(1 / xi_stepsize)
    i = 0
    while i <= (len(xi) - increment):
        # for i in range(len(T_ratio)):
        (ratio_i,) = np.where(T_ratio[i] > 1e-39)
        if len(ratio_i) == len(T_ratio[i]):
            plt.plot(hden_ratio, T_ratio[i], color=colors[i])  # ,
        #       label="xi=10^" + str("%.2f" % xi_lin[i]) + " (all)",
        #     )
        else:
            (else_i,) = np.where(T_ratio[i] < 1e-39)
            plt.plot(
                hden_ratio[0 : else_i[0]], T_ratio[i][0 : else_i[0]], color=colors[i]
            )  # ,
        #     label="xi=10^" + str("%.2f" % xi_lin[i]) + " (all)",
        #  )

        (ratio_i_med,) = np.where(T_ratio_med[i] > 1e-39)
        if len(ratio_i_med) == len(T_ratio_med[i]):
            plt.plot(
                hden_ratio,
                T_ratio_med[i],
                color=colors[i],
                linestyle=":"
                # label="xi=10^" + str("%.2f" % xi_lin[i]) + " (intermediate)",
                # linestyle=":",
            )
        else:
            (else_i_med,) = np.where(T_ratio_med[i] < 1e-39)
            plt.plot(
                hden_ratio[0 : else_i_med[0]],
                T_ratio_med[i][0 : else_i_med[0]],
                color=colors[i],
                linestyle=":"
                #  label="xi=10^" + str("%.2f" % xi_lin[i]) + " (intermediate)",
                #  linestyle=":",
            )

        (ratio_i_noIR,) = np.where(T_ratio_noIR[i] > 1e-39)
        if len(ratio_i_noIR) == len(T_ratio_noIR[i]):
            plt.plot(
                hden_ratio,
                T_ratio_noIR[i],
                color=colors[i],
                linestyle="--"
                #  label="xi=10^" + str("%.2f" % xi_lin[i]) + " (no IR)",
                #  linestyle="--",
            )
        else:
            (else_i_noIR,) = np.where(T_ratio_noIR[i] < 1e-39)
            plt.plot(
                hden_ratio[0 : else_i_noIR[0]],
                T_ratio_noIR[i][0 : else_i_noIR[0]],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (no IR)",
                linestyle="--",
            )
        i += increment

    # plt.plot(hden_ratio, T_ratio[0], color=colors[0], label= ' (' + str(name_index[0]) + ')')
    # plt.plot(hden_ratio, T_ratio_med[0], color=colors[0], label= ' (' + str(name_index[1]) + ')', linestyle=":")
    # plt.plot(hden_ratio, T_ratio_noIR[0], color=colors[0], label= ' (' + str(name_index[2]) + ')', linestyle="--")
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    return ax


def Tmax_Tratio_adjacent(
    hden,
    xi,
    xi_lin,
    avg_temp_split,
    n_transition,
    te_transition,
    avg_temp_split_med,
    n_transition_med,
    te_transition_med,
    avg_temp_split_noIR,
    n_transition_noIR,
    te_transition_noIR,
):
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 14))
    fig.subplots_adjust(hspace=0)
    axs[0].set_title("temperature and ratio vs number density", fontsize=13)
    plt.xlabel("number density $n_h$ [$cm^{-3}$]", fontsize=13)
    axs[0].set_ylabel("$T_{avg} [K]$", fontsize=13)
    axs[0].set_xscale("log")
    axs[0].set_yscale("log")
    i = 0
    colors = plt.cm.rainbow(np.linspace(0, 1, len(avg_temp_split)))
    # for i in range(len(xi)):  # len(xi) rows
    while i <= len(xi):
        row = np.array(avg_temp_split[i])
        (index,) = np.where(row != 1e-30)

        if len(index) == len(row):
            axs[0].plot(
                hden,
                row,
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (all)",
            )
        else:
            (i_1e30,) = np.where(row == 1e-30)
            end = i_1e30[0]
            axs[0].plot(
                hden[index],
                row[0:end],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (all)",
            )

        row_med = np.array(avg_temp_split_med[i])
        (index_med,) = np.where(row_med != 1e-30)
        if len(index_med) == len(row_med):
            axs[0].plot(
                hden,
                row_med,
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (intermediate)",
                linestyle=":",
            )
        else:
            (i_1e30_med,) = np.where(row_med == 1e-30)
            end_med = i_1e30_med[0]
            axs[0].plot(
                hden[index_med],
                row_med[0:end_med],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (intermediate)",
                linestyle=":",
            )

        row_noIR = np.array(avg_temp_split_noIR[i])
        (index_noIR,) = np.where(row_noIR != 1e-30)
        if len(index_noIR) == len(row_noIR):
            axs[0].plot(
                hden,
                row_noIR,
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (no IR)",
                linestyle="--",
            )
        else:
            (i_1e30_noIR,) = np.where(row_noIR == 1e-30)
            end_noIR = i_1e30_noIR[0]
            axs[0].plot(
                hden[index_noIR],
                row_noIR[0:end_noIR],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (no IR)",
                linestyle="--",
            )
    i += 5
    axs[0].scatter(
        n_transition, te_transition, color=colors, marker="*", s=160, label="all"
    )
    axs[0].scatter(
        n_transition_med,
        te_transition_med,
        color=colors,
        marker="o",
        s=100,
        label="intermediate",
    )
    axs[0].scatter(
        n_transition_noIR,
        te_transition_noIR,
        color=colors,
        marker="^",
        s=100,
        label="no IR",
    )
    axs[0].legend(bbox_to_anchor=(1.04, 0.5), loc="upper left", borderaxespad=0)

    T_ratio = np.exp(np.diff(np.log(avg_temp_split)))
    T_ratio_med = np.exp(np.diff(np.log(avg_temp_split_med)))
    T_ratio_noIR = np.exp(np.diff(np.log(avg_temp_split_noIR)))
    hden_ratio = (hden[1:] + hden[:-1]) / 2

    axs[1].set_xscale("log")
    axs[1].set_ylim(0.9, 1.2)
    axs[1].set_ylabel("Ratio (T[i+1] / T[i])", fontsize=13)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(T_ratio)))
    for i in range(len(T_ratio)):
        (ratio_i,) = np.where(T_ratio[i] > 1e-39)
        if len(ratio_i) == len(T_ratio[i]):
            axs[1].plot(
                hden_ratio,
                T_ratio[i],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (all)",
            )
        else:
            (else_i,) = np.where(T_ratio[i] < 1e-39)
            axs[1].plot(
                hden_ratio[0 : else_i[0]],
                T_ratio[i][0 : else_i[0]],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (all)",
            )

        (ratio_i_med,) = np.where(T_ratio_med[i] > 1e-39)
        if len(ratio_i_med) == len(T_ratio_med[i]):
            axs[1].plot(
                hden_ratio,
                T_ratio_med[i],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (intermediate)",
                linestyle=":",
            )
        else:
            (else_i_med,) = np.where(T_ratio_med[i] < 1e-39)
            axs[1].plot(
                hden_ratio[0 : else_i_med[0]],
                T_ratio_med[i][0 : else_i_med[0]],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (intermediate)",
                linestyle=":",
            )

        (ratio_i_noIR,) = np.where(T_ratio_noIR[i] > 1e-39)
        if len(ratio_i_noIR) == len(T_ratio_noIR[i]):
            axs[1].plot(
                hden_ratio,
                T_ratio_noIR[i],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (no IR)",
                linestyle="--",
            )
        else:
            (else_i_noIR,) = np.where(T_ratio_noIR[i] < 1e-39)
            axs[1].plot(
                hden_ratio[0 : else_i_noIR[0]],
                T_ratio_noIR[i][0 : else_i_noIR[0]],
                color=colors[i],
                label="xi=10^" + str("%.2f" % xi_lin[i]) + " (no IR)",
                linestyle="--",
            )
        i += 5
    return axs
