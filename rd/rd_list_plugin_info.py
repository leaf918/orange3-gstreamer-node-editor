import subprocess
import csv

# Run gst-inspect-1.0 command and capture output
output = subprocess.check_output(['/root/miniconda3/bin/gst-inspect-1.0'])
# output = subprocess.run(['gst-inspect-1.0'], shell=False)

# Split output into lines and remove empty lines
lines = [line.strip() for line in output.decode().split('\n') if line.strip()]

# Initialize list of dictionaries to store plugin information
plugins = []

# Loop through lines and extract plugin information
for i, line in enumerate(lines):
    if line.startswith('Plugin '):
        # New plugin found, create new dictionary to store information
        plugin = {'name': line.split(' ')[1], 'description': ''}
        plugins.append(plugin)
    elif line.startswith('Description: '):
        # Add description to current plugin dictionary
        plugins[-1]['description'] = line.split(': ')[1]
    elif i < len(lines) - 1 and lines[i+1].startswith('Rank: '):
        # Add rank to current plugin dictionary (if present)
        plugins[-1]['rank'] = lines[i+1].split(': ')[1]

# Write plugin information to CSV file
with open('plugins.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['name', 'description', 'rank'])
    writer.writeheader()
    for plugin in plugins:
        writer.writerow(plugin)
