import json

# Load the JSON file
file_path = 'sim_dataset_high.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract the unique "instruction" values and store them in a list
unique_instructions = list(set(item['instruction'] for item in data))

# Count the number of unique instructions
instruction_count = len(unique_instructions)

# Print the number of unique instructions and the instructions themselves
print(f"Number of unique instructions: {instruction_count}")
for instruction in unique_instructions:
    print(instruction)

# Now `unique_instructions` is a list containing all the unique instructions
