import numpy as np
import pandas as pd
import os
import csv


# merged files vectors(bidders' payments) and optimal selection and compare if for every non-winner player pi=0
def read_correct(path):

    indexes = [6, 7, 10, 12, 15, 18]

    for i in indexes:

        a = pd.read_csv(path + '//selection_' + str(i) + '.csv')
        b = pd.read_csv(path + '//vectors_' + str(i) + '.csv')
        b = b.dropna(axis=1)
        merged = a.merge(b, on=['N', 'i'])
        merged.to_csv(path + '//merged_' + str(i) + '.csv', index=False)

        csv_path = path + '//merged_' + str(i) + '.csv'
        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            for row in readCSV:

                selection = np.fromstring(row[2].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_vcg = np.fromstring(row[3].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_quadratic = np.fromstring(row[4].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_min_quadratic = np.fromstring(row[5].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_b_nearest = np.fromstring(row[6].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_vcg_nearest = np.fromstring(row[7].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_min_vcg_nearest = np.fromstring(row[8].replace("[", "").replace("]", ""), dtype=float, sep=' ')

                for index in range(len(selection)):
                    if selection[index] == 0:
                        if v_vcg[index] != 0:
                            print("Vcg is wrong at row with index" + str(i))
                        if v_quadratic[index] != 0:
                            print("Quad is wrong at row with index" + str(i))
                        if v_min_quadratic[index] != 0:
                            print("MinQuad is wrong at row with index" + str(i))
                        if v_b_nearest[index] != 0:
                            print("BNearest is wrong at row with index" + str(i))
                        if v_vcg_nearest[index] != 0:
                            print("VCGNearest is wrong at row with index" + str(i))
                        if v_min_vcg_nearest[index] != 0:
                            print("MinVCGNearest is wrong at row with index" + str(i))


# read_correct("folder30_15_high_volumes")
# read_correct("folder30_30_high_volumes")
# read_correct("folder30_small_volumes")
#
# read_correct("folder90_15_high_volumes")
# read_correct("folder90_30_high_volumes")
# read_correct("folder90_small_volumes")


