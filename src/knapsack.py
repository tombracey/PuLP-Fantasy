import pulp
from transform_data import transform_data

constituencies = transform_data()

def knapsack(constituencies, budget, num_constituencies):
    problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

    selection = pulp.LpVariable.dicts("select", range(len(constituencies)), 0, 1, pulp.LpBinary)

    problem += pulp.lpSum([constituencies[i]['Projected_Points'] * selection[i] for i in range(len(constituencies))])

    problem += pulp.lpSum([constituencies[i]['Price'] * selection[i] for i in range(len(constituencies))]) <= budget

    problem += pulp.lpSum([selection[i] for i in range(len(constituencies))]) == num_constituencies

    countries = ['England', 'Scotland', 'Wales']
    for country in countries:
        problem += pulp.lpSum([selection[i] for i in range(len(constituencies)) if constituencies[i]['Country'] == country]) >= 1

    max_same_party = 5
    for party in set([constituency['Winning_Party'] for constituency in constituencies]):
        problem += pulp.lpSum([selection[i] for i in range(len(constituencies)) if constituencies[i]['Winning_Party'] == party]) <= max_same_party

    problem.solve()

    selected_constituencies = [constituencies[i] for i in range(len(constituencies)) if pulp.value(selection[i]) == 1]

    return selected_constituencies

budget = 96964
num_constituencies = 10

best_combo = knapsack(constituencies, budget, num_constituencies)
for constituency in best_combo:
    print(constituency)
