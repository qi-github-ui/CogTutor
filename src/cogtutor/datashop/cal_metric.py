import json
import nltk

nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Load the data
file_path = 'high_output_json_files/merged_generate_high.json'  # replace with your file path
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize counters
total_dialogues = len(data)
total_turns = 0
total_tokens = 0

# Process each dialogue
for dialogue in data:
    dialogue_turns = len(dialogue['dialogue']['dialogue'])
    total_turns += dialogue_turns

    for turn in dialogue['dialogue']['dialogue']:
        tokens = word_tokenize(turn['content'])
        total_tokens += len(tokens)

# Calculate averages
avg_turns_per_dialogue = total_turns / total_dialogues
avg_tokens_per_turn = total_tokens / total_turns

print("Dialogues:", total_dialogues)
print("Total turns:", total_turns)
print("Total tokens:", total_tokens)
print("Avg. turns per dialogue:", avg_turns_per_dialogue)
print("Avg. tokens per turn:", avg_tokens_per_turn)
