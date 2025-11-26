from utils import custom_round

test_cases = [
    (55955, 56000),
    (4158, 4000),
    (4500, 4500),
    (4700, 4700),
    (4200, 4000), # Closer to 4000 (diff 200) than 4500 (diff 300)
    (4300, 4500), # Closer to 4500 (diff 200) than 4000 (diff 300)
    (100, 0), # Closer to 0 (diff 100) than 500 (diff 400)
    (250, 0), # Tie? 0 (diff 250), 500 (diff 250). Code picks first found?
    (251, 500),
]

for price, expected in test_cases:
    result = custom_round(price)
    print(f"Price: {price}, Expected: {expected}, Got: {result}, Match: {result == expected}")
