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




Created on Mon Nov 19 17:32:51 2018

@author: Luca Clissa
"""
"""
========================
SQL DataBase Handler
========================

==================== =========================================================
Utility functions
==============================================================================
create_connection    Connect to a SQLite Database.
select_channel       Extract channels and return data and knots dictionaries.
==================== =========================================================

"""
import os
import sqlite3
import numpy as np

def create_connection(db_file):
    """Create a connection to a SQLite database.

    Keyword arguments:
    db_file: database file
    
    Return values:
    Connection object or None
    """
    
    if db_file.count("/") == 0:
        os.chdir('/home/luca/workspace/DCS_HV/python/')
        print("path: ", os.getcwd())
        print(db_file)
    try:
        #conn = sqlite3.connect('/home/luca/workspace/DCS_HV/python/TILE_DCS_HV-May2017.sqlite')
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("Connection Error")
 
    return None

def select_channel(conn,channel,hvlist=(1,48),metric="sd",resolution=0.5):
    """Filter channels and organize data into dictionaries.
    
    Keyword arguments:
    conn: the Connection object
    channel: the channel to be selected
    hvlist: tuple containing start/end subchannel indexes
    metric: measure that determines whether to add a new knot
    resolution: maximal difference tolerated within same-knot set
    
    Return values:
    data_dict: dictionary with real data as numpy array
    knots_dict: dictionary with endpoints of constant intervals
    
    The function filters the table CONDBR2_F0003_IOVS selecting just
    channels specified in channel and subchannels in the range defi-
    ned in hvlist. Data are stored as is in the dictionary data_dict,
    having keys equal to subchannels colnames and data as values.
    Also they are summarized into homogeneous intervals stored in the
    dictionary knots_dict. Keys are knots identifying interval's end-
    point and values are the relative summary measure. Homogeneity is
    determined by the arguments metric and resolution.
    """
    ### TO DO:
    #    1) add table argument
    #    2) allow for subchannels list rather than range
    #    3) implement try/except approach
    
    start_idx = int(hvlist[0])
    end_idx = int(hvlist[1])
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM CONDBR2_F0003_IOVS')
    # retrieve column headers
    col_names = [cn[0] for cn in cur.description]
    # build the sql statement for selecting variables
    sql_col = (col_names[2]+ ", " + col_names[3] + ", "    # interval timestamp
               + ", ".join(col_names[(start_idx + 8):(end_idx + 9)]))
    var_names = sql_col.split(", ")
    # execute sql command to filter data table
    cur.execute(
            "SELECT {v} FROM CONDBR2_F0003_IOVS where CHANNEL_ID={chan}".format
            (v=sql_col, chan=channel))
    rows = cur.fetchall()    # list of tuples    
    data_matrix = np.array(rows)    # trasform into numpy array
    # initialize output objects
    data_dict = {}
    knots_dict = {}
    
    for i in range(len(data_matrix[0])):
        data_dict[var_names[i]] = data_matrix [:,i]
        
        #knots = np.where( np.diff(data_dict[var_names[i]]) > np.std(data_dict[var_names[i]]) )[0]
        if var_names[i] != 'IOV_SINCE' and var_names[i] != 'IOV_UNTIL':
            if metric == "sd":
                # compute absolute differences between adjacent values
                abs_differences = np.abs( np.diff(data_dict[var_names[i]]))
                knots = np.where(abs_differences 
                                 > min(np.std(data_dict[var_names[i]]),
                                              resolution)
                        )[0]
                knots = list(knots + 1)    # add 1 to set the knot to endpoint
            elif metric == "iqr":
                # compute absolute differences between adjacent values
                abs_differences = np.abs( np.diff(data_dict[var_names[i]]))
                iqr = np.subtract(
                        np.percentile(data_dict[var_names[i]], [75, 25]))
                knots = np.where( abs_differences > min(iqr,resolution) )[0]
                knots = list(knots + 1)
            else:
                print("""ERROR: metric measure not supported. Try standard 
                      deviation <sd> or interquartile range <iqr>""")
            knots.insert(0,0)
            knots.append( len(data_dict[var_names[i]]) -1 )
            knots_dict[var_names[i]] = knots
            
    return [data_dict, knots_dict]