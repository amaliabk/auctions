import numpy as np
import pandas as pd
import os
import math


def ranges_valuations(l_bound, u_bound, bins):
    """
    Determine how to split the valuation ranges into high/low/medium
    categories, for instance if the l_bound is 1, the u_bound is 30 and
    the bins are 3 the output is ((1, 10), (11, 20), (21, 30)).
    
    :param l_bound: The lower bound of valuations' range
    :param u_bound: The upper bound of valuations' range
    :param bins: The number of bins to split the valuations' range
    :return: returns a list of ranges0.
    """
    rng = range(l_bound, u_bound + 1)
    k, m = divmod(len(rng), bins)
    ranges = list(rng[i * k + min(i, m):(i + 1) * k + min(i + 1,
                      m)] for i in range(bins))
    min_max_range = []
    for i in range(len(ranges)):
        min_max_range.append((min(ranges[i]), max(ranges[i])))
    # return the ranges
    return min_max_range


def generate_valuations(N, l_bound, u_bound, bins, p_lower=0.4, p_medium=0.4):

    """
    Determine the bidders' valuations.

    :param N: The number of bidders
    :param l_bound: The lower bound of valuations' range
    :param u_bound: The upper bound of valuations' range
    :param bins: The number of bins to split the valuations' range
    :param p_lower: The percentage of bidders with low valuations-default=0.4
    :param p_medium: The percentage of bidders with medium valuations-default=0.4
    :return: returns a list of valuations
    """

    # determine the cutting points for the intervals of bidders with low,
    # medium and high valuations. The percentages are 0.4, 0.4 and 0.2 for low
    # medium and high valuations respectively
    intervals = pd.qcut(range(N + 1), [0, p_lower, p_lower + p_medium])
    first_cut = int(round(intervals.categories[0].right))
    second_cut = int(round(intervals.categories[1].right))

    ranges_val = ranges_valuations(l_bound, u_bound, bins)

    valuations = np.zeros(N)

    # set the valuations for the bidders. 40% of the bidders will have low
    #  valuations 40%, medium valuations and 20% high valuations in order
    # to mimic real data.
    valuations[0:first_cut] = np.random.randint(ranges_val[0][0],
                                                ranges_val[0][1], first_cut)
    valuations[first_cut:second_cut] = np.random.randint(ranges_val[1][0],
                                                         ranges_val[1][1],
                                                         second_cut - first_cut)
    valuations[second_cut:N] = np.random.randint(ranges_val[2][0],
                                                 ranges_val[2][1],
                                                 N - second_cut)
    return valuations


def generate_volumes(N, weight, p_lower, p_medium, p_hvolume):
    """
    Determine the bidders' volumes.
    :param N: The number of bidders
    :param weight: The mechanism's budget
    :param p_lower: The percentage of bidders with low valuations-default=0.4
    :param p_medium: The percentage of bidders with medium valuations-default=0.4
    :param p_hvolume: The percentage of bidders with high demand
    :return: returns a list of valuations
    """

    # bidders with high volumes
    # it is supposed that 20%, 15% and 30% of bidders has high volumes
    volumes = np.zeros(N)

    # number of bidders with high volumes
    high_volume = int(round(p_hvolume * N))

    # if the volume of all the bidders should be relative small,
    # i.e. w < 1/3 * W
    if p_hvolume == 0:
        # randomly generate the volume of the bidders in the range(1, w/3)
        zero_ind = np.where(volumes == 0)[0]
        temp = np.random.randint(1, weight / 3, len(zero_ind))
        volumes[zero_ind] = temp
        return volumes

    # if 15% of bidders have huge demand
    # randomly select high volumes ranging from W/2 to 0.8 * W
    if p_hvolume == 0.15:
        high = np.random.choice(range(int(math.ceil(weight / 2)),
                                      int(0.8 * weight)), high_volume)

        rest = np.random.choice(range(int(1),
                                      int(weight / 3)), N - high_volume)

        volumes = np.concatenate((high, rest))
        return volumes

    if p_hvolume == 0.30:
        high = np.random.choice(range(int(math.ceil(weight / 2)),
                                      int(0.8 * weight)), high_volume)

        rest = np.random.choice(range(int(1),
                                      int(weight / 3)), N - high_volume)

        volumes = np.concatenate((high, rest))
        return volumes


def generate_data(N, l_bound, u_bound, bins, weight, p_lower, p_medium, p_hvolume):
    """
    Return the bidders' valuations and volumes.

    :param N: The number of bidders
    :param l_bound: The lower bound of valuations' range
    :param u_bound: The upper bound of valuations' range
    :param bins: The number of bins to split the valuations' range
    :param weight: The mechanism's budget
    :param p_lower: The percentage of bidders with low valuations-default=0.4
    :param p_medium: The percentage of bidders with medium valuations-default=0.4
    :return: returns a list of valuations
    """

    valuations = generate_valuations(N, l_bound, u_bound,
                                     bins, p_lower, p_medium)
    volumes = generate_volumes(N, weight, p_lower, p_medium, p_hvolume)
    return valuations, volumes, weight


def create_files(directory, l_bound, u_bound, bins, weight, p_lower,
                 p_medium, p_hvolume):
    if p_hvolume == 0:
        dir_name = directory + "_small_volumes"
    elif p_hvolume == 0.15:
        dir_name = directory + "_15_high_volumes"
    elif p_hvolume == 0.30:
        dir_name = directory + "_30_high_volumes"
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
        for i in [6, 7, 10, 12, 15, 18]:
            name = dir_name + "/data_" + str(i)
            os.makedirs(dir_name + "/data_" + str(i))
            for k in range(1, 16):
                valuations, volumes, weight = generate_data(i, l_bound,
                                                            u_bound, bins,
                                                            weight, p_lower, 
                                                            p_medium,
                                                            p_hvolume
                                                            )
                np.savetxt(name + "/valuations_" + str(i) + "_" + str(k) + ".csv",
                           valuations, delimiter=",")
                np.savetxt(name + "/volumes_" + str(i) + "_" + str(k) + ".csv",
                           volumes, delimiter=",")
                np.savetxt(name + "/weight_" + str(i) + "_" + str(k) + ".csv",
                           np.asarray([weight]), delimiter=",")
        
    else:
        print("Directory already exists. Choose another name!")
        

create_files("folder90", 1, 30, 3, 90, p_lower=0.4, p_medium=0.4, p_hvolume=0)

create_files("folder90", 1, 30, 3, 90, p_lower=0.4,  p_medium=0.4, p_hvolume=0.15)

create_files("folder90", 1, 30, 3, 90, p_lower=0.4, p_medium=0.4, p_hvolume=0.30)

create_files("folder30", 1, 30, 3, 30, p_lower=0.4, p_medium=0.4, p_hvolume=0)

create_files("folder30", 1, 30, 3, 30, p_lower=0.4, p_medium=0.4, p_hvolume=0.15)

create_files("folder30", 1, 30, 3, 30, p_lower=0.4, p_medium=0.4, p_hvolume=0.30)


