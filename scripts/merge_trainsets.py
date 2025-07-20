import os
import glob

input_dirs = [
    os.path.join("data", "trainset", "transcripts"),
    os.path.join("data", "trainset", "synthetic"),
]
output_dir = os.path.join("data", "trainset", "merged")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "merged_trainset.jsonl")

with open(output_file, "w", encoding="utf-8") as outfile:
    for input_dir in input_dirs:
        jsonl_files = glob.glob(os.path.join(input_dir, "*.jsonl"))
        for jsonl_file in jsonl_files:
            with open(jsonl_file, "r", encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)

print(f"Merged trainsets written to {output_file}")
