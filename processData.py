import os
import re
import matplotlib.pyplot as plt

def extract_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        filtered_lines = [line.strip() for line in lines if any(keyword in line for keyword in keywords)]
    return filtered_lines

def extract_numerical_values(line):
    return re.findall(r'\b\d+\.*\d*\b', line)

def process_folder(folder_path):
    data = {keyword: {} for keyword in keywords}
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            extracted_lines = extract_lines(file_path)
            
            for keyword in keywords:
                keyword_lines = [line for line in extracted_lines if keyword in line]
                if keyword_lines:
                    inner_hashmap = {}
                    for line in keyword_lines:
                        numerical_values = extract_numerical_values(line)
                        if numerical_values:
                            key = re.search(r'-(\d+)\.txt', filename).group(1)
                            inner_hashmap[key] = float(numerical_values[0])  # Convert the value to float
                    
                    if inner_hashmap:
                        data[keyword][filename] = inner_hashmap[key]
    
    return data

# List of keywords to search for
keywords = [
    "system.cpu.dcache.overall_misses::total",
    "system.cpu.icache.overall_misses::total",
    "system.l2.overall_misses::total",
    "system.cpu.dcache.overall_miss_rate::total",
    "system.cpu.icache.overall_miss_rate::total",
    "system.l2.overall_miss_rate::total"
]

# Folder path containing the .txt files
folder_path = "/home/011/a/ax/axs230094/hitMissValues"

result_data = process_folder(folder_path)

# Plotting the data using Matplotlib
for keyword, inner_data in result_data.items():
    plt.bar(inner_data.keys(), inner_data.values(), label=keyword)

plt.xlabel('Cacheline Size')
plt.ylabel('Outer Hashmap Key')
plt.title('Graph for Collected Data')
plt.legend()
plt.show()
