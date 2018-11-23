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




Created on Thu Nov 22 10:20:32 2018

@author: Luca Clissa
"""

### TO DO LIST:
# 1) implement the test with a list of modules to import and a loop of 
#    try_import, except and error handling 

def check_libraries_installed():
    try:
        numpy_err = 0
        import numpy
    except ImportError:
        print("IMPORT ERROR: Module numpy not found. Try:")
        print("pip install numpy")
        numpy_err = 1
    try:
        matplotlib_err = 0
        import matplotlib
    except ImportError:
        print("IMPORT ERROR: Module matplotlib not found. Try:")
        print("pip install matplotlib")
        matplotlib_err = 1
    try:
        seaborn_err = 0
        import seaborn
    except ImportError:
        print("IMPORT ERROR: Module seaborn not found. Try:")
        print("pip install seaborn")
        seaborn_err = 1
    finally:
        if (numpy_err+matplotlib_err+seaborn_err) == 0:
            print("All libraries imported successfully")
            
check_libraries_installed()
    