```   ___      ___         __           __      
  / _ \___ / _/__ _____/ /___ ______/ /  ___ 
 / , _/ -_) _/ _ `/ __/ __/ // / __/ _ \/ _ \
/_/|_|\__/_/ \_,_/\__/\__/\_,_/_/ /_.__/\___/
```    

# Prerequisites

- Python 3.8 or higher
- MacOS
- Powermetrics

# Usage

Navigate into the `instrument` directory:
```bash
cd instrument
```

Compile the sampler:
```bash
python3 ./orchestrator.py build
```

Setup the virtual environment:
```bash
python3 -m venv venv
```

Ensure virtual environment is activated:
```bash
source venv/bin/activate
```

Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Run warmup process:
```bash
python3 ./orchestrator.py warmup
```

Run the measurment for command:
```bash
sudo python3 ./orchestrator.py measure "<command to measure>"
```

Run the analysis:
```bash
sudo python3 ./orchestrator.py analyze  
```

Example:
```
sudo python3 ./orchestrator.py measure "java /Users/user/Downloads/refacturbo-experiment/experiments/s1/unoptimized/s1.java"
```