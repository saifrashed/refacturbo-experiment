#!/bin/bash

# Check if a command is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a command to run."
    echo "Usage: $0 <command>"
    exit 1
fi

# Output file for power metrics
OUTPUT_FILE="./data/measurement.txt"

# Function to process powermetrics output
powermetrics_process() {
    previous_timestamp=0

    # Read input from stdin
    while read -r line; do
        # Process each line and extract combined Power (CPU + GPU + ANE)
        pow_W=$(echo "$line" | grep '^Intel energy model derived package power (CPUs+GT+SA):' | grep -oE '[0-9.]+')

        if [[ -n "$pow_W" ]]; then
            # Get timestamp in milliseconds
            current_timestamp=$(date +%s%N | cut -b1-13)
            
            # Append to output file in CSV format: timestamp,power
            echo "$current_timestamp,$pow_W" >> "$OUTPUT_FILE"
        fi
    done
}

# Initialize output file with header
echo "timestamp,power" > "$OUTPUT_FILE"

# Start powermetrics in the background with 500 ms sampling interval
powermetrics --samplers cpu_power -i 500 | powermetrics_process &
# Store the PID of powermetrics
POWERMETRICS_PID=$!

# Run the provided command
"$@"

# Stop powermetrics after the command finishes
kill $POWERMETRICS_PID
wait $POWERMETRICS_PID 2>/dev/null

echo "Power metrics saved to $OUTPUT_FILE"