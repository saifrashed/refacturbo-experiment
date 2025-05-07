#include <IOKit/IOKitLib.h>
#include <libkern/OSByteOrder.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

struct SMCParamStruct {
  enum {
    kSMCUserClientOpen = 0,
    kSMCUserClientClose = 1,
    kSMCHandleYPCEvent = 2,
    kSMCReadKey = 5,
    kSMCGetKeyInfo = 9,
  };

  enum class SMCKey : uint32_t {
    TotalPower = 'PSTR',  // Power: System Total Rail (watts)
    CPUPower = 'PCPC',    // Power: CPU Package CPU (watts)
    iGPUPower = 'PCPG',   // Power: CPU Package GPU (watts)
    CPU1Temp = 'TC1C',    // Temp: CPU Core 1 Temperature (C)
    CPU2Temp = 'TC2C',    // Temp: CPU Core 2 Temperature (C)
    CPU3Temp = 'TC3C',    // Temp: CPU Core 3 Temperature (C)
    CPU4Temp = 'TC4C',    // Temp: CPU Core 4 Temperature (C)
  };

  enum class DataType : uint32_t {
    flt = 'flt ',   // Floating point
    sp78 = 'sp78',  // Fixed point: SIIIIIIIFFFFFFFF
    sp87 = 'sp87',  // Fixed point: SIIIIIIIIFFFFFFF
    spa5 = 'spa5',  // Fixed point: SIIIIIIIIIIFFFFF
  };

  struct SMCVersion {
    unsigned char major;
    unsigned char minor;
    unsigned char build;
    unsigned char reserved;
    unsigned short release;
  };

  struct SMCPLimitData {
    uint16_t version;
    uint16_t length;
    uint32_t cpuPLimit;
    uint32_t gpuPLimit;
    uint32_t memPLimit;
  };

  struct SMCKeyInfoData {
    IOByteCount dataSize;
    DataType dataType;
    uint8_t dataAttributes;
  };

  SMCKey key;
  SMCVersion vers;
  SMCPLimitData pLimitData;
  SMCKeyInfoData keyInfo;
  uint8_t result;
  uint8_t status;
  uint8_t data8;
  uint32_t data32;
  uint8_t bytes[32];
};

float FromSMCFixedPoint(uint8_t* bytes, size_t fraction_bits) {
  return static_cast<int16_t>(OSReadBigInt16(bytes, 0)) /
         static_cast<float>(1 << fraction_bits);
}

class SMCKey {
 public:
  SMCKey(io_object_t connect, SMCParamStruct::SMCKey key)
      : connect_(connect), key_(key) {
    SMCParamStruct out{};
    if (CallSMCFunction(SMCParamStruct::kSMCGetKeyInfo, &out))
      keyInfo_ = out.keyInfo;
  }

  bool Exists() { return keyInfo_.dataSize > 0; }

  float Read() {
    if (!Exists())
      return 0;

    SMCParamStruct out{};
    if (!CallSMCFunction(SMCParamStruct::kSMCReadKey, &out))
      return 0;
    switch (keyInfo_.dataType) {
      case SMCParamStruct::DataType::flt:
        return *reinterpret_cast<float*>(out.bytes);
      case SMCParamStruct::DataType::sp78:
        return FromSMCFixedPoint(out.bytes, 8);
      case SMCParamStruct::DataType::sp87:
        return FromSMCFixedPoint(out.bytes, 7);
      case SMCParamStruct::DataType::spa5:
        return FromSMCFixedPoint(out.bytes, 5);
      default:
        break;
    }
    return 0;
  }

 private:
  bool CallSMCFunction(uint8_t which, SMCParamStruct* out) {
    if (!connect_)
      return false;

    SMCParamStruct in{};
    in.key = key_;
    in.keyInfo.dataSize = keyInfo_.dataSize;
    in.data8 = which;

    size_t out_size = sizeof(*out);
    bool success = IOConnectCallStructMethod(
                       connect_, SMCParamStruct::kSMCHandleYPCEvent, &in,
                       sizeof(in), out, &out_size) == kIOReturnSuccess;

    return success;
  }

  io_object_t connect_;
  SMCParamStruct::SMCKey key_;
  SMCParamStruct::SMCKeyInfoData keyInfo_{};
};

struct Measurement {
  double timestamp;  // Seconds since start
  float total_power; // PSTR (watts)
  float cpu_power;   // PCPC (watts)
  float igpu_power;  // PCPG (watts)
  float cpu1_temp;   // TC1C (C)
  float cpu2_temp;   // TC2C (C)
  float cpu3_temp;   // TC3C (C)
  float cpu4_temp;   // TC4C (C)
};

double get_timestamp() {
  struct timeval tv;
  gettimeofday(&tv, nullptr);
  return tv.tv_sec + tv.tv_usec / 1e6;
}

void take_measurement(SMCKey& PSTR, SMCKey& PCPC, SMCKey& PCPG, SMCKey& TC1C, 
                      SMCKey& TC2C, SMCKey& TC3C, SMCKey& TC4C, 
                      double start_time, std::vector<Measurement>& measurements) {
  Measurement m;
  m.timestamp = get_timestamp() - start_time;
  m.total_power = PSTR.Exists() ? PSTR.Read() : 0;
  m.cpu_power = PCPC.Exists() ? PCPC.Read() : 0;
  m.igpu_power = PCPG.Exists() ? PCPG.Read() : 0;
  m.cpu1_temp = TC1C.Exists() ? TC1C.Read() : 0;
  m.cpu2_temp = TC2C.Exists() ? TC2C.Read() : 0;
  m.cpu3_temp = TC3C.Exists() ? TC3C.Read() : 0;
  m.cpu4_temp = TC4C.Exists() ? TC4C.Read() : 0;
  measurements.push_back(m);
}

void save_measurements(const std::vector<Measurement>& measurements, double start_time, double execution_time = -1) {
  double end_time = get_timestamp();
  double duration = end_time - start_time;
  double total_energy = 0;
  for (size_t i = 1; i < measurements.size(); ++i) {
    double dt = measurements[i].timestamp - measurements[i - 1].timestamp;
    double avg_power = (measurements[i].total_power + measurements[i - 1].total_power) / 2;
    total_energy += avg_power * dt;
  }

  double average_power = duration > 0 ? total_energy / duration : 0;

  std::ofstream out_file("./measurement/measurement.txt");
  if (!out_file) {
    std::cerr << "Failed to open output file" << std::endl;
    return;
  }

  out_file << "Measurement time (sec): " << duration << "\n";
  if (execution_time >= 0) {
    out_file << "Execution time (sec): " << execution_time << "\n";
  }
  out_file << "Total Energy Consumed (joules): " << total_energy << "\n";
  out_file << "Average Power (W): " << average_power << "\n\n";
  out_file << "Timestamp(s),TotalPower(W),CPUPower(W),iGPUPower(W),"
           << "CPU1Temp(C),CPU2Temp(C),CPU3Temp(C),CPU4Temp(C)\n";
  for (const auto& m : measurements) {
    out_file << m.timestamp << "," << m.total_power << "," << m.cpu_power << ","
             << m.igpu_power << "," << m.cpu1_temp << "," << m.cpu2_temp << ","
             << m.cpu3_temp << "," << m.cpu4_temp << "\n";
  }

  out_file.close();
}

int main(int argc, char* argv[]) {
  // Create measurement directory if it doesn't exist
  mkdir("./measurement", 0755);

  // Open SMC service
  io_service_t service = IOServiceGetMatchingService(
      kIOMasterPortDefault, IOServiceMatching("AppleSMC"));
  if (!service) {
    std::cerr << "Failed to find AppleSMC service" << std::endl;
    return 1;
  }

  io_object_t connect;
  if (IOServiceOpen(service, mach_task_self(), 1, &connect) != kIOReturnSuccess) {
    std::cerr << "Failed to open SMC service" << std::endl;
    IOObjectRelease(service);
    return 1;
  }

  if (IOConnectCallMethod(connect, SMCParamStruct::kSMCUserClientOpen,
                          nullptr, 0, nullptr, 0, nullptr, nullptr, nullptr,
                          nullptr) != kIOReturnSuccess) {
    std::cerr << "Failed to open SMC user client" << std::endl;
    IOServiceClose(connect);
    IOObjectRelease(service);
    return 1;
  }

  // Initialize SMC keys
  SMCKey PSTR(connect, SMCParamStruct::SMCKey::TotalPower);
  SMCKey PCPC(connect, SMCParamStruct::SMCKey::CPUPower);
  SMCKey PCPG(connect, SMCParamStruct::SMCKey::iGPUPower);
  SMCKey TC1C(connect, SMCParamStruct::SMCKey::CPU1Temp);
  SMCKey TC2C(connect, SMCParamStruct::SMCKey::CPU2Temp);
  SMCKey TC3C(connect, SMCParamStruct::SMCKey::CPU3Temp);
  SMCKey TC4C(connect, SMCParamStruct::SMCKey::CPU4Temp);

  std::vector<Measurement> measurements;
  double start_time = get_timestamp();
  double execution_time = -1; // Default: no execution time

  // Check for command-line argument
  std::string command;
  if (argc > 1) {
    // Reconstruct command from arguments
    std::stringstream ss;
    for (int i = 1; i < argc; ++i) {
      ss << argv[i];
      if (i < argc - 1) ss << " ";
    }
    command = ss.str();
  }

  if (!command.empty()) {
    // Create pipe to capture command output
    int pipefd[2];
    if (pipe(pipefd) == -1) {
      std::cerr << "Failed to create pipe" << std::endl;
      IOConnectCallMethod(connect, SMCParamStruct::kSMCUserClientClose,
                         nullptr, 0, nullptr, 0, nullptr, nullptr, nullptr, nullptr);
      IOServiceClose(connect);
      IOObjectRelease(service);
      return 1;
    }

    // Execute command and measure until it finishes
    pid_t pid = fork();
    if (pid == -1) {
      std::cerr << "Failed to fork process" << std::endl;
      close(pipefd[0]);
      close(pipefd[1]);
      IOConnectCallMethod(connect, SMCParamStruct::kSMCUserClientClose,
                         nullptr, 0, nullptr, 0, nullptr, nullptr, nullptr, nullptr);
      IOServiceClose(connect);
      IOObjectRelease(service);
      return 1;
    } else if (pid == 0) {
      // Child process: redirect stdout to pipe
      close(pipefd[0]); // Close read end
      dup2(pipefd[1], STDOUT_FILENO); // Redirect stdout to pipe
      close(pipefd[1]); // Close write end after duplication
      execl("/bin/sh", "sh", "-c", command.c_str(), nullptr);
      std::cerr << "Failed to execute command" << std::endl;
      _exit(1);
    } else {
      // Parent process: read from pipe and measure until child finishes
      close(pipefd[1]); // Close write end
      std::stringstream output;
      char buffer[128];
      ssize_t nbytes;

      // Non-blocking read setup
      int flags = fcntl(pipefd[0], F_GETFL, 0);
      fcntl(pipefd[0], F_SETFL, flags | O_NONBLOCK);

      int status;
      while (waitpid(pid, &status, WNOHANG) == 0) {
        // Read available output
        while ((nbytes = read(pipefd[0], buffer, sizeof(buffer) - 1)) > 0) {
          buffer[nbytes] = '\0';
          output << buffer;
        }
        take_measurement(PSTR, PCPC, PCPG, TC1C, TC2C, TC3C, TC4C, start_time, measurements);
        sleep(1); // Sleep for 1s between measurements
      }
      // Read any remaining output
      flags = fcntl(pipefd[0], F_GETFL, 0);
      fcntl(pipefd[0], F_SETFL, flags & ~O_NONBLOCK); // Set to blocking
      while ((nbytes = read(pipefd[0], buffer, sizeof(buffer) - 1)) > 0) {
        buffer[nbytes] = '\0';
        output << buffer;
      }
      close(pipefd[0]); // Close read end

      // Take one final measurement
      take_measurement(PSTR, PCPC, PCPG, TC1C, TC2C, TC3C, TC4C, start_time, measurements);

      // Parse execution time from output
      std::string output_str = output.str();
      std::string prefix = "Execution time: ";
      size_t pos = output_str.find(prefix);
      if (pos != std::string::npos) {
        std::string time_str = output_str.substr(pos + prefix.length());
        std::stringstream time_ss(time_str);
        if (!(time_ss >> execution_time)) {
          std::cerr << "Failed to parse execution time" << std::endl;
        }
      } else {
        std::cerr << "Execution time not found in output" << std::endl;
      }
    }
  } else {
    // No command: measure for 5 seconds
    while (get_timestamp() - start_time < 5.0) {
      take_measurement(PSTR, PCPC, PCPG, TC1C, TC2C, TC3C, TC4C, start_time, measurements);
      sleep(1); // Sleep for 1s between measurements
    }
    // Take one final measurement
    take_measurement(PSTR, PCPC, PCPG, TC1C, TC2C, TC3C, TC4C, start_time, measurements);
  }

  // Save measurements
  save_measurements(measurements, start_time, execution_time);

  // Cleanup
  IOConnectCallMethod(connect, SMCParamStruct::kSMCUserClientClose,
                      nullptr, 0, nullptr, 0, nullptr, nullptr, nullptr, nullptr);
  IOServiceClose(connect);
  IOObjectRelease(service);

  return 0;
}