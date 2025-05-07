#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import time
import signal

from scipy.stats import shapiro

REPETITIONS = 30
COOLDOWN_MS = 5000

def run_command(command, description):
    """Execute a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.stderr:
            print(result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing {description}: {e}")
        print(e.stderr)
        sys.exit(1)

def warmup(duration=10, post_delay=5):
    print("Started: CPU Warm-up")
    start_time = time.time()

    # Perform arithmetic calculations
    result = 0
    for i in range(100000000):
        result += (i * i) % 12345  # Simple but heavy arithmetic
        if time.time() - start_time >= duration:
            break
    print("Ended: CPU Warm-up")
    
    # Wait before returning to ensure stability
    print(f"Waiting {post_delay} seconds before measurements...")
    time.sleep(post_delay)
    print("Ready for measurements")

def measure_baseline(args):
    # warmup()
    print("Started: Measuring baseline")
     # Construct command
    cmd = f"./sampler"
    
    # Run command multiple times with cooldown and rename measurement file
    for i in range(REPETITIONS):
        print(f"Run {i+1}/{REPETITIONS}")
        run_command(cmd, f"Baseline command with path {args.path}")
        
        # Rename measurement.txt to measurement_<index>.txt
        old_file = os.path.join("measurement", "measurement.txt")
        new_file = os.path.join("measurement", f"{i+1}.txt")
        try:
            if os.path.exists(old_file):
                os.rename(old_file, new_file)
            else:
                print(f"Warning: {old_file} not found after run {i+1}")
        except OSError as e:
            print(f"Error renaming {old_file} to {new_file}: {e}")
        
        # Sleep for cooldown period
        if i < REPETITIONS - 1:
            time.sleep(COOLDOWN_MS / 1000.0)

    print("Ended: Measuring baseline")

def measure_java(args):
    # warmup()
    print("Started: Measuring java program")

    # Construct command
    cmd = f"./sampler 'java -cp . {args.path}'"
    
    # Run Java command multiple times with cooldown and rename measurement file
    for i in range(REPETITIONS):
        print(f"Run {i+1}/{REPETITIONS}")
        run_command(cmd, f"Java command with path {args.path}")
        
        # Rename measurement.txt to measurement_<index>.txt
        old_file = os.path.join("measurement", "measurement.txt")
        new_file = os.path.join("measurement", f"{i+1}.txt")
        try:
            if os.path.exists(old_file):
                os.rename(old_file, new_file)
            else:
                print(f"Warning: {old_file} not found after run {i+1}")
        except OSError as e:
            print(f"Error renaming {old_file} to {new_file}: {e}")
        
        # Sleep for cooldown period
        if i < REPETITIONS - 1:
            time.sleep(COOLDOWN_MS / 1000.0)

    print("Ended: Measuring java program")

def analyze_measurements():
    print("Started: Analyzing measurements")
    # Initialize lists to store the four values across all measurements
    measurement_times = []
    execution_times = []
    total_energies = []
    average_powers = []
    
    # Directory containing measurement files
    measurement_dir = "measurement"
    
    # Iterate over the expected measurement files (1.txt to 50.txt)
    for i in range(1, REPETITIONS + 1):
        file_path = os.path.join(measurement_dir, f"{i}.txt")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Warning: Measurement file {file_path} not found")
            continue
        
        try:
            # Read and parse the measurement file
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                # Extract the four key values from the first four lines
                for line in lines[:4]:
                    if line.startswith("Measurement time (sec):"):
                        measurement_times.append(float(line.split(":")[1].strip()))
                    elif line.startswith("Execution time (sec):"):
                        execution_times.append(float(line.split(":")[1].strip()))
                    elif line.startswith("Total Energy Consumed (joules):"):
                        total_energies.append(float(line.split(":")[1].strip()))
                    elif line.startswith("Average Power (W):"):
                        average_powers.append(float(line.split(":")[1].strip()))
        
        except Exception as e:
            print(f"Error reading or parsing {file_path}: {e}")
            continue
            
    
    # Check if any data was collected
    if not measurement_times:
        print("Error: No valid measurement data found")
        return


    # print("\nAnalysis Results:")
    # print(f"Measurement Times (sec): {measurement_times}")
    # print(f"Execution Times (sec): {execution_times}")
    print(f"Total Energy Consumed (joules): {total_energies}")
    # print(f"Average Power (W): {average_powers}")

    # List of datasets and their names
    datasets = [
        (measurement_times, "Measurement Time"),
        (execution_times, "Execution Time"),
        (total_energies, "Total Energy Consumed"),
        (average_powers, "Average Power")
    ]
    
    for data, name in datasets:
        if len(data) < 3:
            print(f"{name}: Sample size too small for Shapiro-Wilk test (n={len(data)})")
            continue
        stat, p_value = shapiro(data)
        normality = "Normal" if p_value > 0.05 else "Not Normal"
        print(f"{name}: W={stat:.4f}, p-value={p_value:.4f}, {normality}")

    print("Ended: Analyzing measurements")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="CLI to run experimenter commands")
    parser.add_argument('command', choices=['build', 'baseline', 'java', 'analyze'], 
                        help="Command to execute: build, baseline, java, or analyze")
    parser.add_argument('--path', help="Absolute path of source code", required=False)

    args = parser.parse_args()

    # Determine the command to execute
    if args.command == 'build':
        run_command("make && ./sampler", "build command")
    elif args.command == 'baseline':
        measure_baseline(args)
    elif args.command == 'java':
        # Check if path is provided
        if not args.path:
            print("Error: --path argument is required for java command")
            sys.exit(1)

        # Validate absolute path
        if not os.path.isabs(args.path):
            print("Error: Provided path must be absolute")
            sys.exit(1)    
        
        measure_java(args)
    elif args.command == 'analyze':
        analyze_measurements()

if __name__ == "__main__":
    main()