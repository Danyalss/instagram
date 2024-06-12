import json

def knapsack(upgrades, max_budget):
    n = len(upgrades)
    dp = {i: 0 for i in range(max_budget + 1)}
    selected = {i: [] for i in range(max_budget + 1)}

    for upgrade in upgrades:
        price = upgrade["price"]
        profit = upgrade["profitPerHourDelta"]
        upgrade_id = upgrade["name"]

        for budget in range(max_budget, price - 1, -1):
            if dp[budget] < dp[budget - price] + profit:
                dp[budget] = dp[budget - price] + profit
                selected[budget] = selected[budget - price] + [upgrade_id]

    return dp[max_budget], selected[max_budget]

# Read data from JSON file using context manager
with open('data.json') as f:
    data = json.load(f)

# Filter upgrades for the knapsack
upgrades = [
    item for item in data["upgradesForBuy"]
    if not item["isExpired"] and item["isAvailable"]
]

max_budget = 10000000
max_profit, selected_upgrades = knapsack(upgrades, max_budget)
print(f"Maximum profit obtainable with a budget of {max_budget} is {max_profit}")
print(f"Selected upgrades: {', '.join(selected_upgrades)}")
