

# Commands to run
make && ./syspower

make && ./smc -h

make &&  ./smc -l 



# Instruction 

./smc -h
Apple System Management Control (SMC) tool 1.01
Usage:
./smc [options]
    -c <spell> : cast a spell
    -q         : attempt to discover 'hidden' keys
    -z         : fuzz all possible keys (or one key using -k)
    -f         : fan info decoded
    -h         : help
    -k <key>   : key to manipulate
    -l         : list all keys and values
    -r         : read the value of a key
    -w <value> : write the specified value to a key
    -v         : version


# 


[TC0c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC1c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC2c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC3c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC4c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC5c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC6c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC7c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC8c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
[TC9c] type [sp78] 73703738 len [ 2] attr [C0] -> ATTR_WRITE|ATTR_READ
CPU Core Temperature from PECI in C°, 1 per physical core
This is a modern key present in e.g. iMacPro1,1.
No Mac models with more than 18 CPU cores were released with this key, but no dumps with more than 10 cores are online.
Most likely the numeration follows with alphabetic characters.


#



https://www.green-coding.io/blog/power-measurement-on-macos/

https://github.com/acidanthera/VirtualSMC/blob/master/Docs/SMCKeys.txt

https://github.com/s4y/syspower

https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/12th-generation-intel-core-processors-datasheet-volume-1-of-2/004/platform-environmental-control-interface/

https://docs.kernel.org/peci/peci.html

https://www-inf.telecom-sudparis.eu/COURS/cen/Mesures/tp-perf.html

# Terms


AppleSMC (Apple System Management Controller) is a critical component in macOS for managing hardware functions, including power and thermal sensors.

IOkit, a framework in macOS, facilitates communication between the operating system and hardware devices, including AppleSMC.


Intel PECI (Platform Environment Control Interface) is a proprietary Intel interface introduced in 2006 with the Intel Core 2 Duo, used for monitoring and managing Intel processors, including reading processor temperature and power consumption data.




# Steps



% 1. Construct 5 patterns
% 2. Select an LLM
% 2. For each pattern make a prompt (Zero shot, One shot, Few shot, CoT)
% 3. Produce 10 samples with LLM
% 4. Collect 50 energy measurements (Using linux-based Perf)
%   - Joules/per second
% 3. 

