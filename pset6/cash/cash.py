from cs50 import get_float

while True:
    change = get_float("Change owed:")
    if change > 0.0:
        break
coins = 0
change = round(int(change * 100))

coins = change // 25
change %= 25

coins += change // 10
change %= 10

coins += change // 5
change %= 5

coins += change // 1
print(coins)