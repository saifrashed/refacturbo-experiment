
# Terms

AppleSMC (Apple System Management Controller) is a critical component in macOS for managing hardware functions, including power and thermal sensors.

IOkit, a framework in macOS, facilitates communication between the operating system and hardware devices, including AppleSMC.

Intel PECI (Platform Environment Control Interface) is a proprietary Intel interface introduced in 2006 with the Intel Core 2 Duo, used for monitoring and managing Intel processors, including reading processor temperature and power consumption data.

# Commands to run
make && ./syspower

make && ./smc -h

make &&  ./smc -l 

# Run the following to execute java program

./syspower java -cp . p1.java


# Some useful links 

https://www.green-coding.io/blog/power-measurement-on-macos/

https://github.com/acidanthera/VirtualSMC/blob/master/Docs/SMCKeys.txt

https://github.com/s4y/syspower

https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/12th-generation-intel-core-processors-datasheet-volume-1-of-2/004/platform-environmental-control-interface/

https://docs.kernel.org/peci/peci.html

https://www-inf.telecom-sudparis.eu/COURS/cen/Mesures/tp-perf.html
