import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import glob


def read_average_revenue(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_average = pd.DataFrame({"N": [], "average_vcg": [], "average_b_nearest": [], "average_quadratic": [],
                                       "average_vcg_nearest": []})

    average_vcg = []
    average_b_nearest = []
    average_quadratic = []
    average_vcg_nearest = []
    n_array = []

    for i in indexes:

        csv_path = path + '//results_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            vcg = 0
            b_nearest = 0
            quadratic = 0
            vcg_nearest = 0
            count = 0

            for row in readCSV:

                vcg = vcg + float(row[2])
                b_nearest = b_nearest + float(row[6])
                quadratic = quadratic + float(row[4])
                vcg_nearest = vcg_nearest + float(row[7])
                count = count + 1

            m_vcg = round(vcg/count, 4)
            m_b_nearest = round(b_nearest/count, 4)
            m_quadratic = round(quadratic/count, 4)
            m_vcg_nearest = round(vcg_nearest/count, 4)

            average_vcg.append(m_vcg)
            average_b_nearest.append(m_b_nearest)
            average_quadratic.append(m_quadratic)
            average_vcg_nearest.append(m_vcg_nearest)
            n_array.append(i)

    data_frame_average.N = n_array
    data_frame_average.average_vcg = average_vcg
    data_frame_average.average_b_nearest = average_b_nearest
    data_frame_average.average_quadratic = average_quadratic
    data_frame_average.average_vcg_nearest = average_vcg_nearest

    data_frame_average = data_frame_average[["N", "average_vcg", "average_b_nearest",
                                             "average_quadratic",
                                             "average_vcg_nearest"]]

    data_frame_average.to_csv(path_or_buf=path + "\\average_revenue.csv",
                              index=False)

    csv_path_1 = path + '//average_revenue.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['average_vcg', 'average_b_nearest', 'average_quadratic', 'average_vcg_nearest'],
                color=['darkgrey', 'indianred', 'goldenrod', 'seagreen'])
    plt.ylabel("Average revenue")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Average revenue with supply=30 and 30% high-demand bidders vs Number of bidders", fontsize=8.8)
    plt.show()


def read_total_average_revenue():

    data_frame_average = pd.DataFrame({"N": [], "average_vcg": [], "average_b_nearest": [], "average_quadratic": [],
                                       "average_vcg_nearest": []})

    paths = ["folder30_15_high_volumes", "folder30_30_high_volumes", "folder30_small_volumes",
             "folder90_15_high_volumes", "folder90_30_high_volumes", "folder90_small_volumes"]
    indexes = [6, 7, 10, 12, 15, 18]

    for i in indexes:
        merged = None
        for path in paths:
            a = pd.read_csv(path + '//results_' + str(i) + '.csv')
            if merged is None:
                merged = a
                continue
            merged = merged.append(a)
        merged.to_csv('results//results_merged_' + str(i) + '.csv', index=False)

    average_vcg = []
    average_b_nearest = []
    average_quadratic = []
    average_vcg_nearest = []
    n_array = []

    for i in indexes:

        csv_path = 'results//results_merged_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            vcg = 0
            b_nearest = 0
            quadratic = 0
            vcg_nearest = 0
            count = 0

            for row in readCSV:
                vcg = vcg + float(row[2])
                b_nearest = b_nearest + float(row[6])
                quadratic = quadratic + float(row[4])
                vcg_nearest = vcg_nearest + float(row[7])
                count = count + 1

            m_vcg = round(vcg / count, 4)
            m_b_nearest = round(b_nearest / count, 4)
            m_quadratic = round(quadratic / count, 4)
            m_vcg_nearest = round(vcg_nearest / count, 4)

            average_vcg.append(m_vcg)
            average_b_nearest.append(m_b_nearest)
            average_quadratic.append(m_quadratic)
            average_vcg_nearest.append(m_vcg_nearest)
            n_array.append(i)

    data_frame_average.N = n_array
    data_frame_average.average_vcg = average_vcg
    data_frame_average.average_b_nearest = average_b_nearest
    data_frame_average.average_quadratic = average_quadratic
    data_frame_average.average_vcg_nearest = average_vcg_nearest

    data_frame_average = data_frame_average[["N", "average_vcg", "average_b_nearest",
                                             "average_quadratic",
                                             "average_vcg_nearest"]]

    data_frame_average.to_csv(path_or_buf="results\\results_average_revenue.csv",
                              index=False)

    csv_path_1 = 'results//results_average_revenue.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')

    df.plot.bar(x='N', y=['average_vcg', 'average_b_nearest', 'average_quadratic', 'average_vcg_nearest'],
                color=['darkgrey', 'indianred', 'goldenrod', 'seagreen'])
    plt.ylabel("Average revenue")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Average revenue vs Number of bidders")
    plt.show()


def read_average_value(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_max_avg = pd.DataFrame({"N": [], "max_avg_quad": [],  "max_avg_min_quad": [],
                                       "max_avg_b_near": [],
                                       "max_avg_vcg_near": [], "max_avg_min_vcg_near": []})

    max_avg_quad = []
    max_avg_min_quad = []
    max_avg_b_near = []
    max_avg_vcg_near = []
    max_avg_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = path + '//max_value_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_quadratic = 0
            max_min_quadratic = 0
            max_b_nearest = 0
            max_vcg_nearest = 0
            max_min_vcg_nearest = 0
            count = 0

            for row in readCSV:

                max_quadratic = max_quadratic + float(row[2])
                max_min_quadratic = max_min_quadratic + float(row[3])
                max_b_nearest = max_b_nearest + float(row[4])
                max_vcg_nearest = max_vcg_nearest + float(row[5])
                max_min_vcg_nearest = max_min_vcg_nearest + float(row[6])
                count = count + 1

            m_quadratic = round(max_quadratic / count, 4)
            m_min_quadratic = round(max_min_quadratic / count, 4)
            m_b_nearest = round(max_b_nearest / count, 4)
            m_vcg_nearest = round(max_vcg_nearest / count, 4)
            m_min_vcg_nearest = round(max_min_vcg_nearest / count, 4)

            max_avg_quad.append(m_quadratic)
            max_avg_min_quad.append(m_min_quadratic)
            max_avg_b_near.append(m_b_nearest)
            max_avg_vcg_near.append(m_vcg_nearest)
            max_avg_min_vcg_near.append(m_min_vcg_nearest)
            n_array.append(i)

    data_frame_max_avg.N = n_array
    data_frame_max_avg.max_avg_quad = max_avg_quad
    data_frame_max_avg.max_avg_min_quad = max_avg_min_quad
    data_frame_max_avg.max_avg_b_near = max_avg_b_near
    data_frame_max_avg.max_avg_vcg_near = max_avg_vcg_near
    data_frame_max_avg.max_avg_min_vcg_near = max_avg_min_vcg_near

    data_frame_max_avg = data_frame_max_avg[["N", "max_avg_quad",  "max_avg_min_quad",
                                             "max_avg_b_near",
                                             "max_avg_vcg_near", "max_avg_min_vcg_near"]]

    data_frame_max_avg.to_csv(path_or_buf=path + "\\max_average.csv",
                              index=False)

    csv_path_1 = path + '//max_average.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_avg_quad', 'max_avg_min_quad', 'max_avg_b_near', 'max_avg_vcg_near',
                          'max_avg_min_vcg_near'], color=['darkgrey', 'indianred', 'goldenrod', 'seagreen', 'brown'])
    plt.ylabel("Max average difference value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Average max value vs Number of bidders")
    plt.show()


def read_total_average_value():

    data_frame_max_avg = pd.DataFrame({"N": [], "max_avg_quad": [], "max_avg_min_quad": [],
                                       "max_avg_b_near": [],
                                       "max_avg_vcg_near": [], "max_avg_min_vcg_near": []})

    paths = ["folder30_15_high_volumes", "folder30_30_high_volumes", "folder30_small_volumes",
             "folder90_15_high_volumes", "folder90_30_high_volumes", "folder90_small_volumes"]
    indexes = [6, 7, 10, 12, 15, 18]

    for i in indexes:
        merged = None
        for path in paths:
            a = pd.read_csv(path + '//max_value_' + str(i) + '.csv')
            if merged is None:
                merged = a
                continue
            merged = merged.append(a)
        merged.to_csv('results//max_merged_' + str(i) + '.csv', index=False)

    max_avg_quad = []
    max_avg_min_quad = []
    max_avg_b_near = []
    max_avg_vcg_near = []
    max_avg_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = 'results//max_merged_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_quadratic = 0
            max_min_quadratic = 0
            max_b_nearest = 0
            max_vcg_nearest = 0
            max_min_vcg_nearest = 0
            count = 0

            for row in readCSV:

                max_quadratic = max_quadratic + float(row[2])
                max_min_quadratic = max_min_quadratic + float(row[3])
                max_b_nearest = max_b_nearest + float(row[4])
                max_vcg_nearest = max_vcg_nearest + float(row[5])
                max_min_vcg_nearest = max_min_vcg_nearest + float(row[6])
                count = count + 1

            m_quadratic = round(max_quadratic / count, 4)
            m_min_quadratic = round(max_min_quadratic / count, 4)
            m_b_nearest = round(max_b_nearest / count, 4)
            m_vcg_nearest = round(max_vcg_nearest / count, 4)
            m_min_vcg_nearest = round(max_min_vcg_nearest / count, 4)

            max_avg_quad.append(m_quadratic)
            max_avg_min_quad.append(m_min_quadratic)
            max_avg_b_near.append(m_b_nearest)
            max_avg_vcg_near.append(m_vcg_nearest)
            max_avg_min_vcg_near.append(m_min_vcg_nearest)
            n_array.append(i)

    data_frame_max_avg.N = n_array
    data_frame_max_avg.max_avg_quad = max_avg_quad
    data_frame_max_avg.max_avg_min_quad = max_avg_min_quad
    data_frame_max_avg.max_avg_b_near = max_avg_b_near
    data_frame_max_avg.max_avg_vcg_near = max_avg_vcg_near
    data_frame_max_avg.max_avg_min_vcg_near = max_avg_min_vcg_near

    data_frame_max_avg = data_frame_max_avg[["N", "max_avg_quad",  "max_avg_min_quad",
                                             "max_avg_b_near",
                                             "max_avg_vcg_near", "max_avg_min_vcg_near"]]

    data_frame_max_avg.to_csv(path_or_buf="results\\max_average_value.csv",
                              index=False)

    csv_path_1 = 'results//max_average_value.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_avg_quad', 'max_avg_min_quad', 'max_avg_b_near', 'max_avg_vcg_near',
                          'max_avg_min_vcg_near'], color=['darkgrey', 'indianred', 'goldenrod', 'seagreen', 'brown'])
    plt.ylabel("Max average difference value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Average max difference payment vs Number of bidders")
    plt.show()


def read_max_value(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_max = pd.DataFrame({"N": [], "max_quad": [], "max_min_quad": [],
                                   "max_b_near": [],
                                   "max_vcg_near": [], "max_min_vcg_near": []})

    max_quad = []
    max_min_quad = []
    max_b_near = []
    max_vcg_near = []
    max_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = path + '//max_value_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_quadratic = 0.0
            max_min_quadratic = 0.0
            max_b_nearest = 0.0
            max_vcg_nearest = 0.0
            max_min_vcg_nearest = 0.0

            for row in readCSV:

                max_quadratic = max(float(row[2]), max_quadratic)
                max_min_quadratic = max(float(row[3]), max_min_quadratic)
                max_b_nearest = max(float(row[4]), max_b_nearest)
                max_vcg_nearest = max(float(row[5]), max_vcg_nearest)
                max_min_vcg_nearest = max(float(row[6]), max_min_vcg_nearest)

            max_quad.append(max_quadratic)
            max_min_quad.append(max_min_quadratic)
            max_b_near.append(max_b_nearest)
            max_vcg_near.append(max_vcg_nearest)
            max_min_vcg_near.append(max_min_vcg_nearest)
            n_array.append(i)

    data_frame_max.N = n_array
    data_frame_max.max_quad = max_quad
    data_frame_max.max_min_quad = max_min_quad
    data_frame_max.max_b_near = max_b_near
    data_frame_max.max_vcg_near = max_vcg_near
    data_frame_max.max_min_vcg_near = max_min_vcg_near

    data_frame_max = data_frame_max[["N", "max_quad",  "max_min_quad",
                                     "max_b_near",
                                     "max_vcg_near", "max_min_vcg_near"]]

    data_frame_max.to_csv(path_or_buf=path + "\\max_.csv",
                          index=False)

    csv_path_1 = path + '//max_.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_quad', 'max_min_quad', 'max_b_near', 'max_vcg_near',
                          'max_min_vcg_near'])
    plt.ylabel("Max value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Max value all vs Number of bidders")
    plt.show()


def read_max_total_value():

    data_frame_max = pd.DataFrame({"N": [], "max_quad": [], "max_min_quad": [],
                                   "max_b_near": [],
                                   "max_vcg_near": [], "max_min_vcg_near": []})

    paths = ["folder30_15_high_volumes", "folder30_30_high_volumes", "folder30_small_volumes",
             "folder90_15_high_volumes", "folder90_30_high_volumes", "folder90_small_volumes"]

    indexes = [6, 7, 10, 12, 15, 18]

    for i in indexes:
        merged = None
        for path in paths:
            a = pd.read_csv(path + '//max_value_' + str(i) + '.csv')
            if merged is None:
                merged = a
                continue
            merged = merged.append(a)
        merged.to_csv('results//max_merged_' + str(i) + '.csv', index=False)

    max_quad = []
    max_min_quad = []
    max_b_near = []
    max_vcg_near = []
    max_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = 'results//max_merged_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_quadratic = 0.0
            max_min_quadratic = 0.0
            max_b_nearest = 0.0
            max_vcg_nearest = 0.0
            max_min_vcg_nearest = 0.0

            for row in readCSV:

                max_quadratic = max(float(row[2]), max_quadratic)
                max_min_quadratic = max(float(row[3]), max_min_quadratic)
                max_b_nearest = max(float(row[4]), max_b_nearest)
                max_vcg_nearest = max(float(row[5]), max_vcg_nearest)
                max_min_vcg_nearest = max(float(row[6]), max_min_vcg_nearest)

            max_quad.append(max_quadratic)
            max_min_quad.append(max_min_quadratic)
            max_b_near.append(max_b_nearest)
            max_vcg_near.append(max_vcg_nearest)
            max_min_vcg_near.append(max_min_vcg_nearest)
            n_array.append(i)

    data_frame_max.N = n_array
    data_frame_max.max_quad = max_quad
    data_frame_max.max_min_quad = max_min_quad
    data_frame_max.max_b_near = max_b_near
    data_frame_max.max_vcg_near = max_vcg_near
    data_frame_max.max_min_vcg_near = max_min_vcg_near

    data_frame_max = data_frame_max[["N", "max_quad",  "max_min_quad",
                                     "max_b_near",
                                     "max_vcg_near", "max_min_vcg_near"]]

    data_frame_max.to_csv(path_or_buf="results\\max_value.csv",
                          index=False)

    csv_path_1 = 'results//max_value.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_quad', 'max_min_quad', 'max_b_near', 'max_vcg_near',
                          'max_min_vcg_near'], color=['darkgrey', 'indianred', 'goldenrod', 'seagreen', 'brown'])
    plt.ylabel("Max value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Max value all vs Number of bidders")
    plt.show()


# read_average_revenue("folder30_15_high_volumes")
# read_average_revenue("folder30_30_high_volumes")
# read_average_revenue("folder30_small_volumes")
#
# read_average_revenue("folder90_15_high_volumes")
# read_average_revenue("folder90_30_high_volumes")
# read_average_revenue("folder90_small_volumes")
#
# read_total_average_revenue()

# read_average_value("folder30_15_high_volumes")
# read_average_value("folder30_30_high_volumes")
# read_average_value("folder30_small_volumes")
#
# read_average_value("folder90_15_high_volumes")
# read_average_value("folder90_30_high_volumes")
# read_average_value("folder90_small_volumes")
#
# read_total_average_value()
#
#
# read_max_value("folder30_15_high_volumes")
# read_max_value("folder30_30_high_volumes")
# read_max_value("folder30_small_volumes")
#
# read_max_value("folder90_15_high_volumes")
# read_max_value("folder90_30_high_volumes")
# read_max_value("folder90_small_volumes")
#
#
# read_max_total_value()
#

# for payments with MRC constraint
def read_average_value_min(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_max_avg = pd.DataFrame({"N": [],  "max_avg_min_quad": [],
                                       "max_avg_b_near": [],
                                       "max_avg_min_vcg_near": []})

    max_avg_min_quad = []
    max_avg_b_near = []

    max_avg_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = path + '//max_value_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_min_quadratic = 0
            max_b_nearest = 0

            max_min_vcg_nearest = 0
            count = 0

            for row in readCSV:

                max_min_quadratic = max_min_quadratic + float(row[3])
                max_b_nearest = max_b_nearest + float(row[4])

                max_min_vcg_nearest = max_min_vcg_nearest + float(row[6])
                count = count + 1

            m_min_quadratic = round(max_min_quadratic / count, 4)
            m_b_nearest = round(max_b_nearest / count, 4)

            m_min_vcg_nearest = round(max_min_vcg_nearest / count, 4)

            max_avg_min_quad.append(m_min_quadratic)
            max_avg_b_near.append(m_b_nearest)

            max_avg_min_vcg_near.append(m_min_vcg_nearest)
            n_array.append(i)

    data_frame_max_avg.N = n_array

    data_frame_max_avg.max_avg_min_quad = max_avg_min_quad
    data_frame_max_avg.max_avg_b_near = max_avg_b_near

    data_frame_max_avg.max_avg_min_vcg_near = max_avg_min_vcg_near

    data_frame_max_avg = data_frame_max_avg[["N", "max_avg_min_quad",
                                             "max_avg_b_near",
                                             "max_avg_min_vcg_near"]]

    data_frame_max_avg.to_csv(path_or_buf=path + "\\max_average.csv",
                              index=False)

    csv_path_1 = path + '//max_average.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_avg_min_quad', 'max_avg_b_near',
                          'max_avg_min_vcg_near'])
    plt.ylabel("Max average difference value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Max average difference value vs Number of bidders")
    plt.show()


def read_total_average_value_min():

    data_frame_max_avg = pd.DataFrame({"N": [], "max_avg_min_quad": [],
                                       "max_avg_b_near": [],
                                       "max_avg_min_vcg_near": []})

    paths = ["folder30_15_high_volumes", "folder30_30_high_volumes", "folder30_small_volumes",
             "folder90_15_high_volumes", "folder90_30_high_volumes", "folder90_small_volumes"]
    indexes = [6, 7, 10, 12, 15, 18]

    for i in indexes:
        merged = None
        for path in paths:
            a = pd.read_csv(path + '//max_value_' + str(i) + '.csv')
            if merged is None:
                merged = a
                continue
            merged = merged.append(a)
        merged.to_csv('results//max_merged_' + str(i) + '.csv', index=False)

    max_avg_min_quad = []
    max_avg_b_near = []

    max_avg_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = 'results//max_merged_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_min_quadratic = 0
            max_b_nearest = 0

            max_min_vcg_nearest = 0
            count = 0

            for row in readCSV:

                max_min_quadratic = max_min_quadratic + float(row[3])
                max_b_nearest = max_b_nearest + float(row[4])

                max_min_vcg_nearest = max_min_vcg_nearest + float(row[6])
                count = count + 1

            m_min_quadratic = round(max_min_quadratic / count, 4)
            m_b_nearest = round(max_b_nearest / count, 4)

            m_min_vcg_nearest = round(max_min_vcg_nearest / count, 4)

            max_avg_min_quad.append(m_min_quadratic)
            max_avg_b_near.append(m_b_nearest)

            max_avg_min_vcg_near.append(m_min_vcg_nearest)
            n_array.append(i)

    data_frame_max_avg.N = n_array

    data_frame_max_avg.max_avg_min_quad = max_avg_min_quad
    data_frame_max_avg.max_avg_b_near = max_avg_b_near

    data_frame_max_avg.max_avg_min_vcg_near = max_avg_min_vcg_near

    data_frame_max_avg = data_frame_max_avg[["N", "max_avg_min_quad",
                                             "max_avg_b_near",
                                             "max_avg_min_vcg_near"]]

    data_frame_max_avg.to_csv(path_or_buf="results\\max_average_value.csv",
                              index=False)

    csv_path_1 = 'results//max_average_value.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_avg_min_quad', 'max_avg_b_near',
                          'max_avg_min_vcg_near'], color=['darkgrey', 'indianred', 'seagreen'])
    plt.ylabel("Max average difference value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Average max difference payment vs Number of bidders")
    plt.show()


def read_max_value_min(path):

    indexes = [6, 7, 10, 12, 15, 18]

    data_frame_max = pd.DataFrame({"N": [], "max_min_quad": [],
                                   "max_b_near": [],
                                   "max_min_vcg_near": []})

    max_min_quad = []
    max_b_near = []
    max_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = path + '//max_value_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_min_quadratic = 0.0
            max_b_nearest = 0.0

            max_min_vcg_nearest = 0.0

            for row in readCSV:

                max_min_quadratic = max(float(row[3]), max_min_quadratic)
                max_b_nearest = max(float(row[4]), max_b_nearest)

                max_min_vcg_nearest = max(float(row[6]), max_min_vcg_nearest)

            max_min_quad.append(max_min_quadratic)
            max_b_near.append(max_b_nearest)

            max_min_vcg_near.append(max_min_vcg_nearest)
            n_array.append(i)

    data_frame_max.N = n_array

    data_frame_max.max_min_quad = max_min_quad
    data_frame_max.max_b_near = max_b_near

    data_frame_max.max_min_vcg_near = max_min_vcg_near

    data_frame_max = data_frame_max[["N", "max_min_quad",
                                     "max_b_near",
                                     "max_min_vcg_near"]]

    data_frame_max.to_csv(path_or_buf=path + "\\max_.csv",
                          index=False)

    csv_path_1 = path + '//max_.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_min_quad', 'max_b_near',
                          'max_min_vcg_near'])
    plt.ylabel("Max value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Max value all vs Number of bidders")
    plt.show()


def read_max_total_value_min():

    data_frame_max = pd.DataFrame({"N": [], "max_min_quad": [],
                                   "max_b_near": [],
                                   "max_min_vcg_near": []})

    paths = ["folder30_15_high_volumes", "folder30_30_high_volumes", "folder30_small_volumes",
             "folder90_15_high_volumes", "folder90_30_high_volumes", "folder90_small_volumes"]

    indexes = [6, 7, 10, 12, 15, 18]

    for i in indexes:
        merged = None
        for path in paths:
            a = pd.read_csv(path + '//max_value_' + str(i) + '.csv')
            if merged is None:
                merged = a
                continue
            merged = merged.append(a)
        merged.to_csv('results//max_merged_' + str(i) + '.csv', index=False)

    max_min_quad = []
    max_b_near = []

    max_min_vcg_near = []
    n_array = []

    for i in indexes:

        csv_path = 'results//max_merged_' + str(i) + '.csv'

        with open(csv_path) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            next(readCSV)

            max_min_quadratic = 0.0
            max_b_nearest = 0.0
            max_min_vcg_nearest = 0.0

            for row in readCSV:

                max_min_quadratic = max(float(row[3]), max_min_quadratic)
                max_b_nearest = max(float(row[4]), max_b_nearest)

                max_min_vcg_nearest = max(float(row[6]), max_min_vcg_nearest)

            max_min_quad.append(max_min_quadratic)
            max_b_near.append(max_b_nearest)

            max_min_vcg_near.append(max_min_vcg_nearest)
            n_array.append(i)

    data_frame_max.N = n_array

    data_frame_max.max_min_quad = max_min_quad
    data_frame_max.max_b_near = max_b_near

    data_frame_max.max_min_vcg_near = max_min_vcg_near

    data_frame_max = data_frame_max[["N", "max_min_quad",
                                     "max_b_near",
                                     "max_min_vcg_near"]]

    data_frame_max.to_csv(path_or_buf="results\\max_value.csv",
                          index=False)

    csv_path_1 = 'results//max_value.csv'

    df = pd.read_csv(csv_path_1, delimiter=',')
    df.plot.bar(x='N', y=['max_min_quad', 'max_b_near',
                          'max_min_vcg_near'],  color=['darkgrey', 'indianred', 'seagreen'])
    plt.ylabel("Max value")
    plt.xlabel("Number of bidders")
    plt.xticks(rotation=0)
    plt.title("Max value all vs Number of bidders")
    plt.show()


# read_average_value_min("folder30_15_high_volumes")
# read_average_value_min("folder30_30_high_volumes")
# read_average_value_min("folder30_small_volumes")
#
# read_average_value_min("folder90_15_high_volumes")
# read_average_value_min("folder90_30_high_volumes")
# read_average_value_min("folder90_small_volumes")

# read_total_average_value_min()

#
# read_max_value_min("folder30_15_high_volumes")
# read_max_value_min("folder30_30_high_volumes")
# read_max_value_min("folder30_small_volumes")
#
# read_max_value_min("folder90_15_high_volumes")
# read_max_value_min("folder90_30_high_volumes")
# read_max_value_min("folder90_small_volumes")
#
