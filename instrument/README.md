



# Usage

Compile the measurement instrument:
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

Run the measurment for baseline:
```bash
python3 ./orchestrator.py baseline
```

Run the measurment for java program:
```bash
python3 ./orchestrator.py --path "<Absolute path>" java
```




1. python3 -m venv venv
2. source venv/bin/activate
3. python3 -m pip install -r requirements.txt
4. python3 -m pip freeze > requirements.txt



python3 ./orchestrator.py --path "/Users/saifrashed/Downloads/uva-master/master-project/refacturbo-experiment/experiments/s1/optimized/s1.java" java