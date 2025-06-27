#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import time
import signal

import numpy as np
from scipy.stats import shapiro

REPETITIONS = 50
COOLDOWN_MS = 5000

BASELINE_EC =  None # 18.7119
BASELINE_T = None # 4.0303

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

def measure(command):
    # warmup()
    print("Started: Measuring command")

    # Construct command
    cmd = f"./sampler.sh {command}"
    
    # Run command multiple times with cooldown and rename measurement file
    for i in range(REPETITIONS):
        print(f"Run {i+1}/{REPETITIONS}")
        run_command(cmd, f"")
        
        # Rename measurement.txt to measurement_<index>.txt
        old_file = os.path.join("data", "measurement.txt")
        new_file = os.path.join("data", f"{i+1}.txt")
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

    print("Ended: Measuring command")

def analyze():
    print("Started: Analyzing measurements")

    durations = []
    average_power = []
    average_joules = []
    average_corrected_joules = []

    for i in range(1, REPETITIONS + 1):
        file_path = os.path.join("data", f"{i}.txt")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Warning: Measurement file {file_path} not found")
            continue
        
        try:
            # Read and parse the measurement file
            with open(file_path, 'r') as file:
                lines = file.readlines()

                powers = []
                timestamps = []

                for line in lines[1:]:
                    values = line.strip().split(',')
                    # Convert to seconds according to Energy = Power (W) * Time (s)
                    timestamps.append(float(values[0]) / 1000.0)
                    # Power
                    powers.append(float(values[1]))
    
                # Calculate duration for this measurement
                duration = timestamps[-1] - timestamps[0]
                durations.append(duration)

                # Calculate average power for this measurement
                power = np.mean(powers)
                average_power.append(power)       

                # Using trapezoidal rule to integrate
                energy = np.trapezoid(powers, timestamps) 
                average_joules.append(energy)

                # Calculate average corrected energy
                corrected_energy = energy - ((BASELINE_EC / BASELINE_T) * duration)
                average_corrected_joules.append(corrected_energy)

        except Exception as e:
            print(f"Error reading or parsing {file_path}: {e}")
            continue
    report = []

    if(durations):
        mean_duration = np.mean(durations)
        std_dev_duration = np.std(durations, ddof=1)
        median_duration = np.median(durations)
        min_duration = np.min(durations)
        max_duration = np.max(durations)
        coeff_var_duration = (std_dev_duration / mean_duration) * 100 if mean_duration else float('inf')

        stat, p_value = shapiro(durations)
        normality = "Normal" if p_value > 0.05 else "Not Normal"

        report.append("\nAnalysis Results for Duration (s):")
        report.append(f"Mean: {mean_duration:.4f}")
        report.append(f"Standard Deviation: {std_dev_duration:.4f}")
        report.append(f"Median: {median_duration:.4f}")
        report.append(f"Min: {min_duration:.4f}")
        report.append(f"Max: {max_duration:.4f}")
        report.append(f"Coefficient of Variation: {coeff_var_duration:.2f}%")
        report.append(f"Shapiro-Wilk: W={stat:.4f}, p-value={p_value:.4f}, {normality}")


    if average_power:
        mean_power = np.mean(average_power)
        std_dev_power = np.std(average_power, ddof=1)
        median_power = np.median(average_power)
        min_val_power = np.min(average_power)
        max_val_power = np.max(average_power)
        coeff_var_power = (std_dev_power / mean_power) * 100 if mean_power else float('inf')

        stat_power, p_value_power = shapiro(average_power)
        normality_power = "Normal" if p_value_power > 0.05 else "Not Normal"

        report.append("\nAnalysis Results for Average Power (W):")
        report.append(f"Mean: {mean_power:.4f}")
        report.append(f"Standard Deviation: {std_dev_power:.4f}")
        report.append(f"Median: {median_power:.4f}")
        report.append(f"Min: {min_val_power:.4f}")
        report.append(f"Max: {max_val_power:.4f}")
        report.append(f"Coefficient of Variation: {coeff_var_power:.2f}%")
        report.append(f"Shapiro-Wilk: W={stat_power:.4f}, p-value={p_value_power:.4f}, {normality_power}")

    if average_joules:
        mean = np.mean(average_joules)
        std_dev = np.std(average_joules, ddof=1)
        median = np.median(average_joules)
        min_val = np.min(average_joules)
        max_val = np.max(average_joules)
        coeff_var = (std_dev / mean) * 100 if mean else float('inf')

        stat, p_value = shapiro(average_joules)
        normality = "Normal" if p_value > 0.05 else "Not Normal"

        report.append("\nAnalysis Results for Average Energy (Joules):")
        report.append(f"Mean: {mean:.4f}")
        report.append(f"Standard Deviation: {std_dev:.4f}")
        report.append(f"Median: {median:.4f}")
        report.append(f"Min: {min_val:.4f}")
        report.append(f"Max: {max_val:.4f}")
        report.append(f"Coefficient of Variation: {coeff_var:.2f}%")
        report.append(f"Shapiro-Wilk: W={stat:.4f}, p-value={p_value:.4f}, {normality}")

    if BASELINE_EC and BASELINE_T:
        mean = np.mean(average_corrected_joules)
        std_dev = np.std(average_corrected_joules, ddof=1)
        median = np.median(average_corrected_joules)
        min_val = np.min(average_corrected_joules)
        max_val = np.max(average_corrected_joules)
        coeff_var = (std_dev / mean) * 100 if mean else float('inf')
        stat, p_value = shapiro(average_corrected_joules)
        normality = "Normal" if p_value > 0.05 else "Not Normal"

        report.append("\nCorrected Energy Consumption (EC):")
        report.append(f"Mean: {mean:.4f}")
        report.append(f"Standard Deviation: {std_dev:.4f}")
        report.append(f"Median: {median:.4f}")
        report.append(f"Min: {min_val:.4f}")
        report.append(f"Max: {max_val:.4f}")
        report.append(f"Coefficient of Variation: {coeff_var:.2f}%")
        report.append(f"Shapiro-Wilk: W={stat:.4f}, p-value={p_value:.4f}, {normality}")


    with open(os.path.join("data", "summary.txt"), 'w') as summary_file:
        for line in report:
            summary_file.write(line + "\n")

    print("Ended: Analyzing measurements")

def get_sample(path):
    print("Started: Getting sample")

    average_joules = []
    average_corrected_joules = []

    for i in range(1, REPETITIONS + 1):

        abs_data_path = os.path.abspath(path)
        
        if not os.path.isdir(abs_data_path):
            raise FileNotFoundError(f"The directory {abs_data_path} does not exist")

        file_path = os.path.join(abs_data_path, f"{i}.txt")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Warning: Measurement file {file_path} not found")
            continue
        
        try:
            # Read and parse the measurement file
            with open(file_path, 'r') as file:
                lines = file.readlines()

                powers = []
                timestamps = []

                for line in lines[1:]:
                    values = line.strip().split(',')
                    # Convert to seconds according to Energy = Power (W) * Time (s)
                    timestamps.append(float(values[0]) / 1000.0)
                    # Power
                    powers.append(float(values[1]))

                # Calculate duration for this measurement
                duration = timestamps[-1] - timestamps[0]

                # Using trapezoidal rule to integrate
                energy = np.trapezoid(powers, timestamps) 
                average_joules.append(energy)

                # Calculate average corrected energy
                corrected_energy = energy - ((BASELINE_EC / BASELINE_T) * duration)
                average_corrected_joules.append(corrected_energy)

        except Exception as e:
            print(f"Error reading or parsing {file_path}: {e}")
            continue
    
    
   # Print each average_joules value on a new line
    for joules in average_corrected_joules:
        print(joules)

    print("Ended: Getting sample")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="CLI to run experimenter commands")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for the 'measure' command
    measure_parser = subparsers.add_parser('measure', help='Measure command')
    measure_parser.add_argument('measure_command', help="Command to execute for measuring")

    # Subparser for the 'get_sample' command
    get_sample_parser = subparsers.add_parser('get_sample', help='Get sample command')
    get_sample_parser.add_argument('sample_path', help="Path for getting sample")  # Added argument

    # Subparsers for 'warmup' and 'analyze'
    subparsers.add_parser('warmup', help='Warmup command')
    subparsers.add_parser('analyze', help='Analyze command')

    args = parser.parse_args()

    # Determine the command to execute
    if args.command == 'measure':
        measure(args.measure_command)
    elif args.command == 'get_sample':
        get_sample(args.sample_path) 
    elif args.command == 'analyze':
        analyze()


if __name__ == "__main__":
    main()
