import json
from concurrent.futures import ThreadPoolExecutor

import requests

def send_long_message(bot_token, chat_id, long_message, max_length=4096):
    messages = [long_message[i:i+max_length] for i in range(0, len(long_message), max_length)]
    for message in messages:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
        response = requests.get(url)
        if response.status_code != 200:
            return f"Error: {response.status_code}, message not sent"
    return "Messages sent successfully"






def knapsack_worker(upgrades, dp, selected, max_budget, start, end):
    local_dp = dp.copy()
    local_selected = selected.copy()
    
    for upgrade in upgrades:
        price = upgrade["price"]
        profit = upgrade["profitPerHourDelta"]
        upgrade_id = upgrade["name"]

        for budget in range(end, start - 1, -1):
            if budget >= price and local_dp[budget] < local_dp[budget - price] + profit:
                local_dp[budget] = local_dp[budget - price] + profit
                local_selected[budget] = local_selected[budget - price] + [upgrade_id]

    return local_dp, local_selected

def merge_results(dp1, dp2, selected1, selected2, max_budget):
    for budget in range(max_budget + 1):
        if dp1[budget] < dp2[budget]:
            dp1[budget] = dp2[budget]
            selected1[budget] = selected2[budget]
    return dp1, selected1

def knapsack(upgrades, max_budget, num_threads):
    n = len(upgrades)
    dp = [0] * (max_budget + 1)
    selected = [[] for _ in range(max_budget + 1)]
    
    chunk_size = max_budget // num_threads
    futures = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            start = i * chunk_size
            end = max_budget if i == num_threads - 1 else (i + 1) * chunk_size - 1
            futures.append(executor.submit(knapsack_worker, upgrades, dp, selected, max_budget, start, end))
        
        for future in futures:
            local_dp, local_selected = future.result()
            dp, selected = merge_results(dp, local_dp, selected, local_selected, max_budget)
    
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
num_threads = 4  # Number of threads to use
max_profit, selected_upgrades = knapsack(upgrades, max_budget, num_threads)

# استفاده از تابع
my_bot_token = "6583320212:AAErFlhIYmA0Je36piZCnXa_C48Jl31-PCk"
chat_id = "1663788795"



print1 = f"Maximum profit obtainable with a budget of {max_budget} is {max_profit}"
print(print1)
send_long_message(my_bot_token, chat_id, print1)

print2 = f"Selected upgrades: {', '.join(selected_upgrades)}"
print(print2)
send_long_message(my_bot_token, chat_id, print2)
