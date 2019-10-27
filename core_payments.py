import cvxpy as cp
import numpy as np
from itertools import chain, combinations
from copy import deepcopy
from knapsack_integer import payments_vcg, read_data
import gurobipy
import time


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    # chain.from_iterable(['ABC', 'DEF']) --> A B C D E F

def allocation_vcg(sizes, valuations, mechanism_budget,
                   indices=None, optimum=[]):
    if indices is not None:
        valuations = [valuations[i] for i in indices]

    if indices is not None:
        sizes = [sizes[i] for i in indices]

    # vector with bidders' valuations for the items
    valuations = np.array(valuations)

    # boolean vector, 1 if the bidder's demand has been satisfied
    selection = cp.Variable(len(sizes), boolean=True)

    # The feasible alternatives are all subsets of bidders
    size_constraint = sizes * selection <= mechanism_budget

    # total utility to maximize
    utility = valuations * selection

    # the problem to solve, i.e maximize social welfare
    auction = cp.Problem(cp.Maximize(utility), [size_constraint])

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False)

    values = np.round(list(selection.value))
    if len(optimum) > 0:
        optimum = [optimum[i] for i in indices]
        return np.sum(values * valuations) - np.sum(optimum)
    else:
        return values


def selection_vcg(sizes, valuations, mechanism_budget, indices=None, optimum=[]):

    if indices is not None:
        valuations = [valuations[i] for i in indices]

    if indices is not None:
        sizes = [sizes[i] for i in indices]

    # vector with bidders' valuations for the items
    valuations = np.array(valuations)

    # boolean vector, 1 if the bidder's demand has been satisfied
    selection = cp.Variable(len(sizes), boolean=True)

    # The feasible alternatives are all subsets of bidders
    size_constraint = sizes * selection <= mechanism_budget

    # total utility to maximize
    utility = valuations * selection

    # the linear problem to solve, i.e maximize social welfare
    auction = cp.Problem(cp.Maximize(utility), [size_constraint])

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False)

    values = np.round(list(selection.value))

    return selection.value


def test(indices, initial_indices, sizes, valuations, mechanism_budget, optimal_allocation, prices):
    complementary_indices = set(initial_indices) - set(indices)
    return cp.sum(prices[np.array(list(complementary_indices))]) >= allocation_vcg(sizes, valuations,
                                                                                   mechanism_budget,
                                                                                   indices,
                                                                                   optimal_allocation)


def core_revenue(sizes, valuations, mechanism_budget):

    selection = selection_vcg(sizes, valuations, mechanism_budget, indices=None, optimum=[])

    # create power set of all bidders
    power_set = powerset(range(len(valuations)))

    optimal_allocation = (allocation_vcg(sizes, valuations,
                                         mechanism_budget)) * valuations

    initial_indices = set(range(len(valuations)))

    # boolean vector, 1 if the bidder's demand has been satisfied
    prices = cp.Variable(len(sizes))

    constraints = []
    allocation = {}

    # bid for item should be grater than the respective price
    constraints += [optimal_allocation >= prices]

    # core constraint for every possible subset of bidders
    time1 = time.process_time()

    for indices in power_set:
        if len(indices) > 0 and not initial_indices.issubset(set(indices)):
            complementary_indices = set(initial_indices) - set(indices)
            allocated = allocation_vcg(sizes, valuations, mechanism_budget,
                                       indices, optimal_allocation)
            allocation[indices] = allocated
            constraints += [
                cp.sum(prices[np.array(list(complementary_indices))]) >= allocated
            ]

    time2 = time.process_time()
    print("Time to find core: ", (time2-time1))
    print("Number of constraints:", len(constraints))

    # the linear problem to solve, i.e minimize sum of prices
    auction = cp.Problem(cp.Minimize(cp.sum(prices)), constraints)

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False,

                           eps=1e-10, max_iters=1000000)

    print("core revenue:", sum(p.value for p in prices))

    return np.asarray(prices.value), allocation


def quadratic_payments(sizes, valuations, mechanism_budget, allocation):

    # create power set of all bidders
    power_set = powerset(range(len(valuations)))

    optimal_allocation = (allocation_vcg(sizes, valuations,
                                         mechanism_budget)) * valuations

    initial_indices = set(range(len(valuations)))

    # boolean vector, 1 if the bidder's demand has been satisfied
    prices = cp.Variable(len(sizes))

    constraints = []

    # bid for item should be grater than the respective price
    constraints += [optimal_allocation >= prices]

    # core constraint for every possible subset of bidders
    for indices in power_set:
        if len(indices) > 0 and not initial_indices.issubset(set(indices)):
            complementary_indices = set(initial_indices) - set(indices)
            constraints += [
                cp.sum(prices[np.array(list(complementary_indices))]) >= allocation[indices]
            ]

    print("Number of constraints:", len(constraints))

    # the linear problem to solve, i.e minimize  square sum of prices
    auction = cp.Problem(cp.Minimize(cp.sum(cp.square(prices))), constraints)

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False,
                           eps=1e-10, max_iters=1000000)

    print(sum(p.value for p in prices))

    return np.asarray(prices.value)


def quadratic_min_payments(sizes, valuations, mechanism_budget, core_sum, allocation):

    # create power set of all bidders
    power_set = powerset(range(len(valuations)))

    optimal_allocation = (allocation_vcg(sizes, valuations,
                                         mechanism_budget)) * valuations

    initial_indices = set(range(len(valuations)))

    # boolean vector, 1 if the bidder's demand has been satisfied
    prices = cp.Variable(len(sizes))

    constraints = []

    # bid for item should be grater than the respective price
    constraints += [optimal_allocation >= prices]

    # enforce the revenue to be the minimum (MRC constraint)
    constraints += [cp.sum(prices) == core_sum]

    # core constraint for every possible subset of bidders
    for indices in power_set:
        if len(indices) > 0 and not initial_indices.issubset(set(indices)):
            complementary_indices = set(initial_indices) - set(indices)
            constraints += [
                cp.sum(prices[np.array(list(complementary_indices))]) >= allocation[indices]
            ]

    # the linear problem to solve, i.e minimize  square sum of prices
    auction = cp.Problem(cp.Minimize(cp.sum(cp.square(prices))), constraints)

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False,
                           eps=1e-10, max_iters=1000000)

    print(sum(p.value for p in prices))

    return np.asarray(prices.value)


def b_nearest_payments(sizes, valuations, mechanism_budget, core_sum, allocation):

    # create power set of all bidders
    power_set = powerset(range(len(valuations)))

    optimal_allocation = (allocation_vcg(sizes, valuations,
                                         mechanism_budget)) * valuations

    initial_indices = set(range(len(valuations)))

    # boolean vector, 1 if the bidder's demand has been satisfied
    prices = cp.Variable(len(sizes))

    constraints = []

    # bid for item should be grater than the respective price
    constraints += [optimal_allocation >= prices]

    # enforce the revenue to be the minimum (MRC constraint)
    constraints += [cp.sum(prices) == core_sum]

    # core constraint for every possible subset of bidders
    for indices in power_set:
        if len(indices) > 0 and not initial_indices.issubset(set(indices)):
            complementary_indices = set(initial_indices) - set(indices)
            constraints += [
                cp.sum(prices[np.array(list(complementary_indices))]) >= allocation[indices]
            ]

    # the linear problem to solve, i.e minimize  square sum of prices
    auction = cp.Problem(cp.Minimize(cp.sum(cp.square(prices - valuations))), constraints)

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False,
                           eps=1e-10, max_iters=1000000)

    print(sum(p.value for p in prices))

    return np.asarray(prices.value)


def vcg_nearest_payments(sizes, valuations, mechanism_budget, allocation):

    # create power set of all bidders
    power_set = powerset(range(len(valuations)))

    optimal_allocation = (allocation_vcg(sizes, valuations,
                                         mechanism_budget)) * valuations

    initial_indices = set(range(len(valuations)))

    # boolean vector, 1 if the bidder's demand has been satisfied
    prices = cp.Variable(len(sizes))

    constraints = []

    # bid for item should be grater than the respective price
    constraints += [optimal_allocation >= prices]

    # core constraint for every possible subset of bidders
    for indices in power_set:
        if len(indices) > 0 and not initial_indices.issubset(set(indices)):
            complementary_indices = set(initial_indices) - set(indices)
            constraints += [
                cp.sum(prices[np.array(list(complementary_indices))]) >= allocation[indices]
            ]

    payment_vcg = allocation_vcg(sizes, valuations, mechanism_budget, indices=None, optimum=[])

    # the linear problem to solve, i.e minimize  square sum of prices
    auction = cp.Problem(cp.Minimize(cp.sum(cp.square(prices - payment_vcg))), constraints)

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False,
                           eps=1e-10, max_iters=1000000)

    print(sum(p.value for p in prices))

    return np.asarray(prices.value)


def vcg_min_nearest_payments(sizes, valuations, mechanism_budget, core_sum, allocation):

    # create power set of all bidders
    power_set = powerset(range(len(valuations)))

    optimal_allocation = (allocation_vcg(sizes, valuations,
                                         mechanism_budget)) * valuations

    initial_indices = set(range(len(valuations)))

    # boolean vector, 1 if the bidder's demand has been satisfied
    prices = cp.Variable(len(sizes))

    constraints = []

    # bid for item should be grater than the respective price
    constraints += [optimal_allocation >= prices]

    # enforce the revenue to be the minimum (MRC constraint)
    constraints += [cp.sum(prices) == core_sum]

    # core constraint for every possible subset of bidders
    for indices in power_set:
        if len(indices) > 0 and not initial_indices.issubset(set(indices)):
            complementary_indices = set(initial_indices) - set(indices)
            constraints += [
                cp.sum(prices[np.array(list(complementary_indices))]) >= allocation[indices]
            ]

    payment_vcg = allocation_vcg(sizes, valuations, mechanism_budget, indices=None, optimum=[])

    # the linear problem to solve, i.e minimize  square sum of prices
    auction = cp.Problem(cp.Minimize(cp.sum(cp.square(prices - payment_vcg))), constraints)

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False,
                           eps=1e-10, max_iters=1000000)

    print(sum(p.value for p in prices))

    return np.asarray(prices.value)


def print_results(sizes, valuations, mechanism_budget):

    print("-------Selection-------")
    selection = selection_vcg(sizes, valuations, mechanism_budget)
    print(selection)

    print("\n")

    optimal_allocation = allocation_vcg(sizes, valuations, mechanism_budget)
    print("-------Payments VCG-------")
    payment_vcg = payments_vcg(optimal_allocation, valuations, sizes, mechanism_budget)
    print(payment_vcg)
    print(np.sum(payment_vcg))
    print("\n")

    print("-------Core Payments-------")
    payment_core = core_revenue(sizes, valuations, mechanism_budget)
    print(payment_core)
    print("\n")

    print("-------Quadratic Payments-------")
    payment_quadratic = quadratic_payments(sizes, valuations, mechanism_budget)
    print(payment_quadratic)
    print("\n")

    print("-------Quadratic Minimum Payments-------")
    payment_min_quadratic = quadratic_min_payments(sizes, valuations, mechanism_budget)
    print(payment_min_quadratic)
    print("\n")

    print("-------B Nearest Payments-------")
    payment_b_nearest = b_nearest_payments(sizes, valuations, mechanism_budget)
    print(payment_b_nearest)
    print("\n")

    print("-------VCG Nearest Payments-------")
    payment_vcg_nearest = vcg_nearest_payments(sizes, valuations, mechanism_budget)
    print(payment_vcg_nearest)
    print("\n")

    print("-------VCG Minimum Nearest Payments-------")
    payment_vcg_min_nearest = vcg_min_nearest_payments(sizes, valuations, mechanism_budget)
    print(payment_vcg_min_nearest)
    print("\n")


# data_no = 3
# path = "data\data_"+ str(data_no)
# mechanism_budget, optimal, sizes, valuations = read_data(path, data_no)
# print_results(sizes, valuations, mechanism_budget)
