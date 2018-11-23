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




Created on Mon Nov 19 17:12:02 2018

@author: Luca Clissa
"""

"""
========================
Python Objects Handler
========================

==================== =========================================================
Utility functions
==============================================================================
save_object          Save object from environment to local server.
get_object           Load pickle file from local server into environment.
==================== =========================================================

"""
### TO DO:
#    1) implement try/except controls for errors handling --> verify possible 
#       errors
#    2) add get_object function to retrieve results
#    3) add explicit return
#    4) add docstring

import pickle

def save_object(obj_name, filename):
    """Save python obj_name to the file and path specified in filename."""
     with open(filename+".pkl", 'wb') as output:  # Overwrites any existing file.
#    try:
        pickle.dump(obj_name, output, pickle.HIGHEST_PROTOCOL)
#    except:
#        print("Some error has occurred")
#        return status
            
def get_object(filename, obj_name):
    """Retrieve filename from local disk and store it in obj_name."""
    with open(filename+".pkl", 'rb') as input:
        return pickle.load(input)

        