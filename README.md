
   ___      ___         __           __      
  / _ \___ / _/__ _____/ /___ ______/ /  ___ 
 / , _/ -_) _/ _ `/ __/ __/ // / __/ _ \/ _ \
/_/|_|\__/_/ \_,_/\__/\__/\_,_/_/ /_.__/\___/
                                             

# Usage

Navigate into the `instrument` directory:
```bash
cd instrument
```

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



# Terms

AppleSMC (Apple System Management Controller) is a critical component in macOS for managing hardware functions, including power and thermal sensors.

IOkit, a framework in macOS, facilitates communication between the operating system and hardware devices, including AppleSMC.

Intel PECI (Platform Environment Control Interface) is a proprietary Intel interface introduced in 2006 with the Intel Core 2 Duo, used for monitoring and managing Intel processors, including reading processor temperature and power consumption data.


# Some useful links 

https://www.green-coding.io/blog/power-measurement-on-macos/

https://github.com/acidanthera/VirtualSMC/blob/master/Docs/SMCKeys.txt

https://github.com/s4y/syspower

https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/12th-generation-intel-core-processors-datasheet-volume-1-of-2/004/platform-environmental-control-interface/

https://docs.kernel.org/peci/peci.html

https://www-inf.telecom-sudparis.eu/COURS/cen/Mesures/tp-perf.html
