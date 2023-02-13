# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:35:37 2022

@author: Hina
"""
import numpy as np 
import matplotlib.pyplot as plt
def incident(path, filename):
    file = open(path + '/' + filename + '_out_ang.txt' )
    file.readline()
    Cont_nu, incident, trans, DiffOut, net_trans, reflec, total, reflin, outlin, lineID, cont, nLine = np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])
    for line in file:
        line = line.rstrip('\n')
        line = line.split('\t')
        Cont_nu = np.append(Cont_nu, float(line[0]))
        incident = np.append(incident, float(line[1]))
        trans = np.append(trans, float(line[2]))
        DiffOut = np.append(DiffOut, float(line[3]))
        net_trans = np.append(net_trans, float(line[4]))
        reflec = np.append(DiffOut, float(line[5]))
        total = np.append(total, float(line[6]))
        reflin = np.append(reflin, float(line[7]))
        outlin = np.append(outlin, float(line[8]))
        lineID = np.append(lineID, line[9])
        cont = np.append(cont, line[10])
        nLine = np.append(nLine, float(line[11]))
    return Cont_nu, incident, total, net_trans

def inc_vs_keV(name_index, Cont_nu, incident):
    fig, ax = plt.subplots(figsize=(8, 6))
    #ax.set(title='AGN incident continuum vs energy', xlabel='Energy [KeV]', ylabel='$4\pi \\nu$ $J_{\\nu} $ [erg $cm^{-2} s^{-1}$ ]')
    ax.tick_params(axis='x', labelsize= 18) 
    ax.tick_params(axis='y', labelsize= 18)

    plt.title(str(name_index[3]) + " incident continuum vs energy at $\\xi$=5", fontsize=18)
    plt.xlabel('log$_{10}$(E/[KeV])', fontsize=18)
    plt.ylabel('log$_{10}(4\pi \\nu$ $J_{\\nu} $/[erg $cm^{-2} s^{-1}$ ])', fontsize=18)
    #plt.ylabel(r'log($\frac{E}{KeV}$)', fontsize=14)
    plt.plot(np.log10(Cont_nu), np.log10(incident), label='a(x)=-1.0', linewidth=3)
    #plt.scatter(Cont_nu[n]/13.6, incident[n])
    #plt.text(Cont_nu[n]/1e6, incident[n], str(Cont_nu[n]/1e6) + ',' + str(incident[n]))
    #plt.xlim(-3, 6)
    #plt.xlim(1e-3, 1e6)
    #plt.ylim(1e-4, 1e2)
    plt.xlim(-3, 6)
    #plt.xscale('log')
    #plt.yscale('log')
    return ax
    
def inc_vs_keV_3(name_index, Cont_nu1, incident1, Cont_nu2, incident2, Cont_nu3, incident3):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.tick_params(axis='x', labelsize= 18) 
    ax.tick_params(axis='y', labelsize= 18)
    
    plt.title(str(name_index[3]) + " total continuum vs energy at $\\xi$=5", fontsize=18)
    plt.xlabel('log$_{10}$(E/[KeV])', fontsize=18)
    plt.ylabel('log$_{10}(4\pi \\nu$ $J_{\\nu} $/[erg $cm^{-2} s^{-1}$ ])', fontsize=18)
    plt.plot(np.log10(Cont_nu1), np.log10(incident1), label=str(name_index[0]), linewidth=3)
    plt.plot(np.log10(Cont_nu2), np.log10(incident2), label=str(name_index[1]), linewidth=3)
    plt.plot(np.log10(Cont_nu3), np.log10(incident3), label=str(name_index[2]), linewidth=3)
    #plt.scatter(Cont_nu[n]/13.6, incident[n])
    #plt.text(Cont_nu[n]/1e6, incident[n], str(Cont_nu[n]/1e6) + ',' + str(incident[n]))
    #plt.xlim(-3, 6)
    plt.xlim(1e-3, 1e6)
    #plt.ylim(1e-4, 1e2)
    plt.xlim(.5, 1)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.legend(fontsize = 17, frameon=False)
    return ax

def trans(path, filename):
    file = open(path + '/' + filename + '_out_ang.txt' )
    file.readline()
    Cont_nu, trans = np.array([]),np.array([])
    for line in file:
        line = line.rstrip('\n')
        line = line.split('\t')
        Cont_nu = np.append(Cont_nu, float(line[0]))
        trans = np.append(trans, float(line[1]))
    return Cont_nu, trans