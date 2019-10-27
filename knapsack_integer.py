import cvxpy as cp
import numpy as np
import gurobipy
import os


def read_data(path, data_no):

    with open(path + "\capacity_" + str(data_no) + ".txt") as f:
        for line in f:
            print(line)
            mechanism_budget = (int(float(line.strip())))
    with open(path + "\optimal_" + str(data_no) + ".txt") as f:
        for line in f:
            optimal = (int(float(line.strip())))

    sizes = []
    with open(path + "\weights_" + str(data_no) + ".txt") as f:
        for line in f:
            sizes.append((int(float(line.strip()))))
    sizes = np.array(sizes)

    valuations = []
    with open(path + "\profits_" + str(data_no) + ".txt") as f:
        for line in f:
            valuations.append((int(float(line.strip()))))

    return mechanism_budget, optimal, sizes, valuations


def allocation_vcg(sizes, valuations, mechanism_budget):

    # vector with bidders' valuations for the items
    valuations = np.array(valuations)

    # boolean vector, 1 if the bidder's demand has been satisfied
    selection = cp.Variable(len(sizes), boolean=True)

    # The feasible alternatives are all subsets of bidders of
    # total size <= mechanism_budget
    size_constraint = sizes * selection <= mechanism_budget

    # total utility to maximize
    utility = valuations * selection

    # the problem to solve, i.e maximize social welfare
    auction = cp.Problem(cp.Maximize(utility), [size_constraint])

    # solve the problem with a proper solver
    result = auction.solve(solver=cp.GUROBI, verbose=False)
    # GUROBI:Optimizer is a commercial optimization solver for linear programming (LP)

    values = np.round(list(selection.value))
    # returns the floating point number rounded off to the given n-digits after the decimal point
    return values


def payments_vcg(selection, valuations, sizes, mechanism_budget):

    payment = np.zeros(len(selection))

    # Return a new array of given shape and type, with zeros
    valuations = np.array(valuations)
    for i in range(len(selection)):
        if selection[i] == 1:
            new_valuations = np.delete(valuations, i)
            new_sizes = np.delete(sizes, i)
            new_selection = allocation_vcg(new_sizes,
                                           new_valuations, mechanism_budget)

            # Optimal welfare (for the other players) if player i was not
            # participating.
            new_profit = np.sum(new_selection * new_valuations)
            old_indices = np.array(np.where(selection == 1))
            old_indices = old_indices[0][np.where(old_indices != i)[1]]

            # Welfare of the other players from the chosen outcome
            old_profit = np.sum(selection[old_indices] * valuations[old_indices])
            payment[i] = new_profit - old_profit

    return payment


def print_results(selection, sizes, valuations, mechanism_budget, optimal):
    print("-------Optimal selection-------")
    print(np.where(selection == 1)[0])
    print("\n")

    profit = np.sum(selection * valuations)
    print("-------Profit-------")
    print(profit)
    print("\n")

    if optimal == profit:
        print("The solution is optimal!")
    else:
        print("Non optimal solution!")
    print("\n")

    payment = payments_vcg(selection, valuations, sizes, mechanism_budget)
    print("-------Payments-------")
    print(payment)
    print("\n")

    payoff = valuations - payment
    payoff[np.array(np.where(selection == 0))[0]] = 0
    print("-------Payoffs-------")
    print(payoff)
    print("\n")


# data_no = 3
# path = "data\data_"+ str(data_no)
# mechanism_budget, optimal, sizes, valuations = read_data(path, data_no)
# selection = allocation_vcg(sizes, valuations, mechanism_budget)
# print_results(selection, sizes, valuations, mechanism_budget, optimal)

