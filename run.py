import os
import sys
import subprocess
import time
BASE_PATH = "/home/zzz/ChampSim-hawkeye/"
RESULT_PATH = BASE_PATH + "results_250M/"
RESULT_FILE = RESULT_PATH + "results"
# LOG_PATH = "log/"
#TRACES_PATH  = "/home/cxu-serve/p1/leu-cache/tools/zzz/poly-trace/"
TRACES_PATH = "/home/zzz/traces/poly"
max_sim_core = 12

list_l1i_pref = ['no'] #'no', 'next_line'
list_l1d_pref = ['no']
list_l2c_pref = ['no']
list_llc_pref = ['no']
branch_pred = 'bimodal'
# list_cache_repl = ['lru', 'hawkeye', 'ship', 'ship++', 'drrip', 'srrip']
list_cache_repl = ['srrip']
num_cores = 1
run_instr = 250 #million
skip_instr = 50 #million
list_trace_file = os.listdir(TRACES_PATH)

list_run_setting = []

# Generate ChampSim binaries and run_settings
# os.system("mkdir -p " + RESULT_PATH)
# os.chdir(RESULT_PATH)
for llc_pref in list_llc_pref:
  for l2c_pref in list_l2c_pref:
    for l1d_pref in list_l1d_pref:
      for l1i_pref in list_l1i_pref:
        for cache_repl in list_cache_repl:
          setting = branch_pred + " " +  l1i_pref + " " + l1d_pref + " " + l2c_pref + " " + llc_pref + " " + cache_repl + " " + str(num_cores)
          #print("Current Setting: " + setting)
          # Generate ChampSim binary
          os.system("./build_champsim.sh " + setting)
          # ./run_champsim.sh hashed_perceptron-no-no-no-no-lru-1core 50 50 spec_x264_001.champsimtrace.xz
          # Run binary with trace files
          for trace_file in list_trace_file:
            #print("   Current Trace File:  " + trace_file)
            run_cmd = branch_pred + "-" +  l1i_pref + "-" + l1d_pref + "-" + l2c_pref + "-" + llc_pref + "-" + cache_repl + "-" + str(num_cores) + "core" + " " + str(skip_instr) + " " + str(run_instr) + " " + trace_file
            list_run_setting.append(run_cmd)
            #os.system("./run_champsim.sh " + branch_pred + "-" +  l1i_pref + "-" + l1d_pref + "-" + l2c_pref + "-" + llc_pref + "-" + cache_repl + "-" + str(num_cores) + "core" + " " + str(skip_instr) + " " + str(run_instr) + " " + trace_file)

processes = set()

for run_setting in list_run_setting:
  # print(run_setting)
  run_setting = run_setting.split()
  processes.add(subprocess.Popen(["./run_champsim.sh", run_setting[0], run_setting[1],run_setting[2], run_setting[3]]))
  if len(processes) >= max_sim_core:
    os.wait()
    processes.difference_update([p for p in processes if p.poll() is not None])
  # os.system("./run_champsim.sh " + run_setting)

# Extract results from log files (Do this separately for now)
  #os.system("python " + BASE_PATH + "extract_info.py" + " " + RESULT_PATH + trace_file + "-" + setting + " | tee -a " + RESULT_FILE + ".csv")
