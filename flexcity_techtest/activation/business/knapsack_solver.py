from ortools.algorithms.python import knapsack_solver

def get_assets_knapsack_solver(activable_assets, volume):

    # To make activation_cost integers, we can multiply them by a large constant. This does not change the optimal solution, but allows us to use the knapsack solver that only accepts integers.
    # We assume that activation_costs have at most 3 decimal places, so multiplying by 1000 is sufficient to keep the precision.
    values = [int(asset.activation_cost * 1000) for asset in activable_assets]
    weights = [[asset.volume for asset in activable_assets]]

    # Our problem is NOT a maximization problem, but the minimization of costs that overflow the volume.
    # To use the knapsack solver, we can compute the asset that would be excluded in the optimal solution.
    # This way, selecting the cheapest assets that fill the volume is equivalent to excluding the most expensive assets that exceed the volume.

    total_available_capacity = sum([asset.volume for asset in activable_assets])
    capacities = [total_available_capacity - volume]

    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER,
        "KnapsackExample",
    )

    solver.init(values, weights, capacities)

    try:
        computed_value = solver.solve()
    except ValueError:
        # the solver cannot find a solution, the volume cannot be filled with the available assets.
        # This case should already be handled by the check in strategy.py.
        raise Exception("Not enough capacity available")

    # select the assets that are NOT selected by the solver
    selected_assets = list(activable_assets)
    for i in range(len(activable_assets)):
        if solver.best_solution_contains(i):
            selected_assets.remove(activable_assets[i])

    return selected_assets
