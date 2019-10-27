# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 09:32:27 2018
,b
@author: Stratos - PC
"""

import numpy as np
import os

from knapsack_integer import read_data, allocation_vcg


def test_optimality():
    files = 0
    root_path = os.getcwd()+"\data"
    for _, dirnames, filenames in os.walk(root_path):
        files += len(dirnames)
    for i in range(1, files + 1):
        path = root_path + "\data_"+ str(i)
        mechanism_budget, optimal, sizes, valuations = read_data(path, i)
        selection = allocation_vcg(sizes, valuations, mechanism_budget)
        profit = np.sum(selection * valuations)
        if optimal != profit:
            print("Error in file" + i + ". Non optimal solution!")
            return
    print("Optimality test: Pass")
    
test_optimality()

