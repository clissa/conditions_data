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




Created on Mon Nov 26 16:02:19 2018

@author: Luca Clissa
"""
# import standard python libraries
import os
import sys
import time
import numpy as np

# import user-defined modules
import importlib
pyobj = importlib.import_module("001_py_object_handler", package=None)
dbhandler = importlib.import_module("002_sqldb_handler", package=None)
pcwreg = importlib.import_module("003_piecewise_regression", package=None)


def main():
    database = "TILE_DCS_HV_2017.sqlite"
    # create a database connection
    conn = dbhandler.create_connection(database)
    os.chdir('/home/luca/Desktop/Dottorato/Ricerca/conditions_data/DCS_HV/DCS_CD_Reducer/')
    if not os.path.exists('diagnostic_plots_2017'):
        os.mkdir('diagnostic_plots_2017')

    if not os.path.exists('results_2017'):
        os.mkdir('results_2017')
    
    for channel in range(int(sys.argv[1]),int(sys.argv[2])):
        with conn:
            data_dict, knots_dict = dbhandler.select_channel(conn,channel)
        
        exec_time=[]
        start = time.time()
        pcwreg.piecewise_reg(data_dict,knots_dict,channel,diagnostics=True)
        end = time.time()
        
        exec_time.append(end-start)
        if channel==(int(sys.argv[2]) -1):
            print("AVERAGE RUNNING TIME PER CHANNEL:")
            print(np.mean(exec_time))
 
if __name__ == '__main__':
    main()

