import random

# Step 1: Define participants with their stake
validators = {
    "Alice": 50,   # 50% chance
    "Bob": 30,     # 30% chance
    "Charlie": 20  # 20% chance
}

# Step 2: Calculate total stake
total_stake = sum(validators.values())

# Step 3: Generate a random number between 1 and total_stake
pick = random.randint(1, total_stake)

# Step 4: Loop through validators and pick one based on weighted stake
current = 0
selected_validator = None

for validator, stake in validators.items():
    current += stake  # Increase cumulative weight
    if pick <= current:
        selected_validator = validator
        break  # Stop the loop once a validator is selected

# Step 5: Output result
print("Validators and Stakes:", validators)
print("Random Number Picked:", pick)
print("Selected Validator for block creation:", selected_validator)