#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Copyright 2018 Luca Clissa

This file is part of DCS_CD_Reducer.

DCS_CD_Reducer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DCS_CD_Reducer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DCS_CD_Reducer.  If not, see <https://www.gnu.org/licenses/>.




Created on Mon Nov 19 17:37:35 2018

@author: Luca Clissa
"""
"""
========================
Piecewise regression
========================

==================== =========================================================
Utility functions
==============================================================================
pred_dict            Dictionary with reproduced data.
performance_dict     Dictionary with various measures of Goodness of Fit.
==================== =========================================================
"""
# import standard python modules
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as bckend

# import user-defined modules
import importlib
pyobj = importlib.import_module("001_py_object_handler", package=None)

def piecewise_reg(data,knots,channel,diagnostics=True):
    """Train the model using Nadaraya-Watson estimator.
    
    Keyword arguments:
    data: data dictionary
    knots: knots dictionary
    channel: knots dictionary
    diagnostics: whether to produce diagnostic plots or not
    dictionary with couples [knot, pred_value]
    
    Return valus:
    pred_dict: dictionary with data reproduced by the estimator
    performance_dict: dictionary with various performance measures
    """
    ### TO DO:
    #    1) add argument for output file name
    #    2) plots using seaborn
    
    # initialize empty dictionaries for results
    pred_dict = {}
    performance_dict = {}
    keys = sorted(data.keys())
    # check control variable for diagnostic plots    
    if diagnostics:
        pdf = bckend.PdfPages("""./diagnostic_plots_2017/
                              diagnostic_hv_channel{}.pdf""".format(channel))
    # loop on photomultipliers
    for var in list(keys)[:-2]: #    exclude t_min and t_max        
        pred = []
        pred_vec = np.zeros(len(data[var]))
        # loop on photomultiplier's knots
        for i in range (len( knots[var] ) -1):
            start = knots[var][i]
            end = knots[var][i+1] 
            pred.append([knots[var][i+1], np.mean(data[var][start:end])])
            if end == (len(data[var]) - 1):
                end += 1
            pred_vec[start:end] = np.mean(data[var][start:end])
        
        pred_dict[var] = pred
        perc_err = (data[var] - pred_vec)/(data[var]+.0001)
        performance_dict[var] = { "MAE" : np.mean(abs(data[var] - pred_vec)),
                                  "MSE" : np.mean((data[var] - pred_vec)**2),
                                  "MAX" : np.max(abs(data[var] - pred_vec)),
                                  "MPE" : np.mean(perc_err)}
        
        if diagnostics:
            xlab=np.asarray(data["IOV_SINCE"], dtype='datetime64[ns]')
            plt.figure(1)
            plt.subplot(2,1,1)
            plt.subplots_adjust(top=0.92, bottom=0.15, left=0.15, right=0.95, 
                                hspace=0.25,wspace=0.35)
            plt.plot(xlab, data[var], 'bo', xlab, pred_vec, 'r^', markersize=5)
            plt.ylabel("Voltage")
            #plt.xlabel("Time")
    #        label = real_vs_pred.xaxis.get_major_ticks()[2].label
    #        label.set_orientation('vertical')
            plt.title("Real (blue) VS Predicted (red)", fontsize=8, 
                      fontweight="bold")
            plt.text(xlab[5], pred_vec[0]+1, var)
            plt.subplot(2,1,2)
            plt.subplots_adjust(top=0.88, bottom=0.12, left=0.15, right=0.95, 
                                hspace=0.25,wspace=0.35)
            plt.plot(xlab, perc_err, 'gs', markersize=5)
            plt.ylabel("Percentage error")
            plt.xlabel("Time")
            plt.title("Percentage error over time", fontsize=8, 
                      fontweight="bold")
            # save dignostic plots          
            pdf.savefig(1)
            plt.close()

    # save pred_dict and performance_dict in an external file
    print(os.getcwd())
    pyobj.save_object(pred_dict, """./results_2017/
                pred_dict_channel_{}.pkl""".format(channel))
    pyobj.save_object(performance_dict, """./results_2017/
                performance_dict_channel_{}.pkl""".format(channel))
    
    return pred_dict, performance_dict
