from knapsack_integer import allocation_vcg, payments_vcg
from core_payments import core_revenue, quadratic_payments, quadratic_min_payments, b_nearest_payments,\
     vcg_nearest_payments, vcg_min_nearest_payments, selection_vcg
import numpy as np
import pandas as pd
import os
import csv
import time


def read_data(path):
    folders = [x[0] for x in os.walk(path)]
    folders = folders[1:]
    for folder in folders:

        initial_time = time.process_time()
        data_frame_selection = pd.DataFrame({"N": [], "i": [], "selection": []})

        data_frame = pd.DataFrame({"N": [], "i": [],
                                   "vcg": [], "core": [], "quadratic": [], "min_quadratic": [], "b_nearest": [],
                                   "vcg_nearest": [], "min_vcg_nearest": [],
                                   "volumes": [], "valuations": []})

        data_frame_vectors = pd.DataFrame({"N": [], "i": [],
                                           "v_vcg": [],
                                           "v_quadratic": [], "v_min_quadratic": [], "v_b_nearest": [],
                                           "v_vcg_nearest": [], "v_min_vcg_nearest": [],
                                           "volumes": [], "valuations": []})

        print(folder)
        n = folder.split("data_", 1)[1]
        print("N:", n)
        selection = []
        vcg = []
        core = []
        quadratic = []
        min_quadratic = []
        b_nearest = []
        vcg_nearest = []
        min_vcg_nearest = []
        v_vcg = []
        v_quadratic = []
        v_min_quadratic = []
        v_b_nearest = []
        v_vcg_nearest = []
        v_min_vcg_nearest = []

        val = []
        vol = []
        for i in range(1, 16):
            loop_time = time.process_time()
            # similar = []
            valuations = []
            with open(folder + "\\valuations_" + str(n) + "_" + str(i) + ".csv") as f:
                for line in f:
                    valuations.append((int(float(line.strip()))))

            with open(folder + "\\weight_" + str(n) + "_" + str(i) + ".csv") as f:
                for line in f:
                    mechanism_budget = (int(float(line.strip())))

            weights = []
            with open(folder + "\\volumes_" + str(n) + "_" + str(i) + ".csv") as f:
                for line in f:
                    weights.append((int(float(line.strip()))))
            weights = np.array(weights)

            optimal_allocation = allocation_vcg(weights, valuations,
                                                mechanism_budget)
            payment_vcg = payments_vcg(optimal_allocation, valuations,
                                       weights, mechanism_budget)
            optimal_selection = selection_vcg(weights, valuations, mechanism_budget)

            selection.append(optimal_selection)
            v_vcg.append(payment_vcg)
            vcg.append(np.sum(payment_vcg))

            before_core = time.process_time()

            payment_core, core_constraints = core_revenue(weights, valuations, mechanism_budget)
            core_sum = np.sum(payment_core)
            core.append(core_sum)

            after_core = time.process_time()
            print("Time to find core: ", print_time(before_core, after_core))

            payment_quadratic = quadratic_payments(weights, valuations, mechanism_budget, core_constraints)
            quadratic.append(np.sum(payment_quadratic))
            v_quadratic.append(payment_quadratic)

            after_quad = time.process_time()
            print("Time to find quadratic: ", print_time(after_core, after_quad))

            payment_min_quadratic = quadratic_min_payments(weights, valuations, mechanism_budget, core_sum, core_constraints)
            min_quadratic.append(np.sum(payment_min_quadratic))
            v_min_quadratic.append(payment_min_quadratic)

            after_min_quad = time.process_time()
            print("Time to find min_quadratic: ", print_time(after_quad, after_min_quad))

            payment_b_nearest = b_nearest_payments(weights, valuations, mechanism_budget, core_sum, core_constraints)
            b_nearest.append(np.sum(payment_b_nearest))
            v_b_nearest.append(payment_b_nearest)

            after_b_nearest = time.process_time()
            print("Time to find b_nearest: ", print_time(after_min_quad, after_b_nearest))

            payment_vcg_nearest = vcg_nearest_payments(weights, valuations, mechanism_budget, core_constraints)
            vcg_nearest.append(np.sum(payment_vcg_nearest))
            v_vcg_nearest.append(payment_vcg_nearest)

            after_vcg_nearest = time.process_time()
            print("Time to find vcg_nearest: ", print_time(after_b_nearest, after_vcg_nearest))

            payment_vcg_min_nearest = vcg_min_nearest_payments(weights, valuations, mechanism_budget, core_sum, core_constraints)
            min_vcg_nearest.append(np.sum(payment_vcg_min_nearest))
            v_min_vcg_nearest.append(payment_vcg_min_nearest)

            after_vcg_min = time.process_time()
            print("Time to vcg_min_nearest: ", print_time(after_vcg_nearest, after_vcg_min))

            val.append(valuations)
            vol.append(weights)

            total = time.process_time()
            print("Total time for loop: ", print_time(loop_time, total))

        final = time.process_time()
        print("Total time for ALL loops: ", print_time(initial_time, final))

        data_frame.N = len(range(1, 16)) * [n]
        data_frame.i = list(range(1, 16))
        data_frame.vcg = vcg
        data_frame.core = core
        data_frame.quadratic = quadratic
        data_frame.min_quadratic = min_quadratic
        data_frame.b_nearest = b_nearest
        data_frame.vcg_nearest = vcg_nearest
        data_frame.min_vcg_nearest = min_vcg_nearest
        data_frame.valuations = val
        data_frame.volumes = vol

        data_frame_vectors.N = len(range(1, 16)) * [n]
        data_frame_vectors.i = list(range(1, 16))
        data_frame_vectors.v_vcg = v_vcg
        data_frame_vectors.v_quadratic = v_quadratic
        data_frame_vectors.v_min_quadratic = v_min_quadratic
        data_frame_vectors.v_b_nearest = v_b_nearest
        data_frame_vectors.v_vcg_nearest = v_vcg_nearest
        data_frame_vectors.v_min_vcg_nearest = v_min_vcg_nearest
        data_frame_vectors.valuations = val
        data_frame_vectors.volumes = vol

        data_frame_selection.N = len(range(1, 16)) * [n]
        data_frame_selection.i = list(range(1, 16))
        data_frame_selection.selection = selection

        data_frame = data_frame[["N", "i",
                                 "vcg", "core", "quadratic", "min_quadratic", "b_nearest",
                                 "vcg_nearest", "min_vcg_nearest",
                                 "volumes", "valuations"]]

        data_frame_vectors = data_frame_vectors[["N", "i",
                                                 "v_vcg", "v_quadratic",
                                                 "v_min_quadratic", "v_b_nearest",
                                                 "v_vcg_nearest", "v_min_vcg_nearest",
                                                 "volumes", "valuations"]]

        data_frame_selection = data_frame_selection[["N", "i", "selection"]]

        # the total revenue produced by each mechanism
        data_frame.to_csv(path_or_buf=path + "\\results_" + str(n) + ".csv",
                          index=False)

        # bidders' payments produced by each mechanism
        data_frame_vectors.to_csv(path_or_buf=path + "\\vectors_" + str(n) + ".csv",
                                  index=False)

        # optimal selection
        data_frame_selection.to_csv(path_or_buf=path + "\\selection_" + str(n) + ".csv",
                                    index=False)


# difference revenue of the mechanism in relation to vcg revenue
def read_data_diff_revenue(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_difference = pd.DataFrame({"N": [], "i": [],
                                          "diff_b_nearest": [], "diff_quadratic": [],
                                          "diff_vcg_nearest": []})

    for i in indexes:
        csv_path = path + '//results_' + str(i) + '.csv'
        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            diff_quadratic = []
            diff_b_nearest = []
            diff_vcg_nearest = []


            next(readCSV)

            for row in readCSV:

                vcg = row[2]
                quadratic = row[4]
                b_nearest = row[6]
                vcg_nearest = row[7]

                d_quad = float(quadratic) - float(vcg)
                d_b_nearest = float(b_nearest) - float(vcg)
                d_vcg_nearest = float(vcg_nearest) - float(vcg)

                diff_quadratic.append("{0:.4f}".format(d_quad))
                diff_b_nearest.append("{0:.4f}".format(d_b_nearest))
                diff_vcg_nearest.append("{0:.4f}".format(d_vcg_nearest))

            data_frame_difference.N = len(range(1, 16)) * [i]
            data_frame_difference.i = list(range(1, 16))
            data_frame_difference.diff_quadratic = diff_quadratic
            data_frame_difference.diff_b_nearest = diff_b_nearest
            data_frame_difference.diff_vcg_nearest = diff_vcg_nearest

            data_frame_difference = data_frame_difference[["N", "i",
                                                           "diff_quadratic",
                                                           "diff_b_nearest",
                                                           "diff_vcg_nearest"]]

            data_frame_difference.to_csv(path_or_buf=path + "\\diff_revenue_" + str(i) + ".csv",
                                         index=False)


# determine max(pi - pi(vcg)) for each mechanism
def read_data_max_value(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_max = pd.DataFrame({"N": [], "i": [],
                                   "max_quadratic": [], "max_min_quadratic": [],
                                   "max_b_nearest": [],
                                   "max_vcg_nearest": [], "max_min_vcg_nearest": []})

    for i in indexes:
        csv_path = path + '//vectors_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            max_quadratic = []
            max_min_quadratic = []
            max_b_nearest = []
            max_vcg_nearest = []
            max_min_vcg_nearest = []

            next(readCSV)

            for row in readCSV:

                v_vcg = np.fromstring(row[2].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_quadratic = np.fromstring(row[3].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_min_quadratic = np.fromstring(row[4].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_b_nearest = np.fromstring(row[5].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_vcg_nearest = np.fromstring(row[6].replace("[", "").replace("]", ""), dtype=float, sep=' ')
                v_min_vcg_nearest = np.fromstring(row[7].replace("[", "").replace("]", ""), dtype=float, sep=' ')

                m_quad = np.subtract(v_quadratic, v_vcg)
                m_min_quad = np.subtract(v_min_quadratic, v_vcg)
                m_b_nearest = np.subtract(v_b_nearest, v_vcg)
                m_vcg_nearest = np.subtract(v_vcg_nearest, v_vcg)
                m_min_vcg_nearest = np.subtract(v_min_vcg_nearest, v_vcg)

                max_quadratic.append(np.around(np.amax(m_quad), decimals=4))
                max_min_quadratic.append(np.around(np.amax(m_min_quad), decimals=4))
                max_b_nearest.append(np.around(np.amax(m_b_nearest), decimals=4))
                max_vcg_nearest.append(np.around(np.amax(m_vcg_nearest), decimals=4))
                max_min_vcg_nearest.append(np.around(np.amax(m_min_vcg_nearest), decimals=4))

            data_frame_max.N = len(range(1, 16)) * [i]
            data_frame_max.i = list(range(1, 16))
            data_frame_max. max_quadratic = max_quadratic
            data_frame_max. max_min_quadratic = max_min_quadratic
            data_frame_max. max_b_nearest = max_b_nearest
            data_frame_max. max_vcg_nearest = max_vcg_nearest
            data_frame_max. max_min_vcg_nearest = max_min_vcg_nearest

            data_frame_max = data_frame_max[["N", "i",
                                             "max_quadratic", "max_min_quadratic",
                                             "max_b_nearest",
                                             "max_vcg_nearest", "max_min_vcg_nearest"]]

            data_frame_max.to_csv(path_or_buf=path + "\\max_value_" + str(i) + ".csv",
                                  index=False)


def print_time(time1, time2):
    days = divmod(time2-time1, 86400)  # Get days (without [0]!)
    hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
    minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
    seconds = divmod(minutes[1], 1)  # Use remainder of minutes to calc seconds
    return "Time between dates: %d days, %d hours, %d minutes and %d seconds" % (days[0], hours[0], minutes[0], seconds[0])

#
# read_data("folder30_15_high_volumes")
# read_data("folder30_30_high_volumes")
# read_data("folder30_small_volumes")
#
# read_data("folder90_15_high_volumes")
# read_data("folder90_30_high_volumes")
# read_data("folder90_small_volumes")


# read_data_diff_revenue("folder30_15_high_volumes")
# read_data_diff_revenue("folder30_30_high_volumes")
# read_data_diff_revenue("folder30_small_volumes")
#
# read_data_diff_revenue("folder90_15_high_volumes")
# read_data_diff_revenue("folder90_30_high_volumes")
# read_data_diff_revenue("folder90_small_volumes")
#
# read_data_max_value("folder30_15_high_volumes")
# read_data_max_value("folder30_30_high_volumes")
# read_data_max_value("folder30_small_volumes")
#
# read_data_max_value("folder90_15_high_volumes")
# read_data_max_value("folder90_30_high_volumes")
# read_data_max_value("folder90_small_volumes")













