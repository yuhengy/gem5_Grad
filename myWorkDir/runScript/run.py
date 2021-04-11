
import os
import time



GEM5_DIR = os.getcwd()

#----------------------
RUN_MODE = "singleProc" # singleProc, multiProc

REDIRECT_TERMINAL_OUTPUT = False

runOpt = ' --cpu-type=DerivO3CPU  \
           --num-cpus=1 \
           --caches --l1d_size=32kB --l1i_size=32kB \
           --l1d_assoc=8 --l1i_assoc=8 \
           --l2cache \
           --l2_size=1MB --l2_assoc=16 \
           --mem-size=4GB'

rstCktOpt = ' --checkpoint-restore=1'

#rekMOpt = ' --l2reKeyMiss --l2_mshrs=%d --l2_max_evict_per_epoch=%d' % (1024*1024 / 64 + 20, 1024*1024 / 64 * 100)
rekMOpt = ' --l2reKeyMiss --l2_mshrs=%d --l2_max_evict_per_epoch=%d' % (1024*1024 / 64 + 20, 2)
rekHOpt = ' --l2reKeyHit --l2_mshrs=%d --l2_max_evict_per_epoch=%d' % (1024*1024 / 64 + 20, 2)

experimentList = []
## SEPT1 hello
#experimentList.append([0, 'X86/gem5.opt', runOpt, 'hello', ''])
#experimentList.append([1, 'X86/gem5.opt', runOpt + rekMOpt, 'hello', ''])
#experimentList.append([2, 'X86/gem5.opt', runOpt + rekHOpt, 'hello', ''])
#experimentList.append([3, 'RISCV/gem5.opt', runOpt, 'hello', ''])
experimentList.append([4, 'RISCV/gem5.opt', runOpt + rstCktOpt, 'hello', ''])
#experimentList.append([4, 'RISCV/gem5.opt', runOpt + rekMOpt, 'hello', ''])
#experimentList.append([5, 'RISCV/gem5.opt', runOpt + rekHOpt, 'hello', ''])

## STEP2 stream
#experimentList.append([6, 'RISCV/gem5.opt', runOpt, 'stream', ''])
experimentList.append([7, 'RISCV/gem5.opt', runOpt + rstCktOpt, 'stream', ''])
#experimentList.append([7, 'RISCV/gem5.opt', runOpt + rekMOpt, 'stream', ''])
#experimentList.append([8, 'RISCV/gem5.opt', runOpt + rekHOpt, 'stream', ''])

#----------------------


def initClient(RUN_MODE):
  from dask.distributed import Client, LocalCluster

  # STEP1 choose a cluster
  if RUN_MODE == "multiProc":
    cluster = LocalCluster(threads_per_worker=1, local_directory="/tmp")
  else:
    assert(False)

  time.sleep(1)
  print(cluster)

  # STEP2 setup a client
  client = Client(cluster)

  return client


def runSimu(index_binary_config_app_arg):
  command = GEM5_DIR + '/build/' + index_binary_config_app_arg[1] + \
    ' --outdir='+ GEM5_DIR + '/myWorkDir/result/' + str(index_binary_config_app_arg[0]) + '-' + index_binary_config_app_arg[3] + \
    ' ' + GEM5_DIR + '/configs/example/se.py' + index_binary_config_app_arg[2] + \
    ' --checkpoint-dir=' + GEM5_DIR + '/myWorkDir/app/' + index_binary_config_app_arg[3] + \
    ' -c ' + GEM5_DIR + '/myWorkDir/app/' + index_binary_config_app_arg[3] + '/build/' + index_binary_config_app_arg[3] + ' --options="' + index_binary_config_app_arg[4] +'"'

  if REDIRECT_TERMINAL_OUTPUT:
    command += ' > ' + GEM5_DIR + '/myWorkDir/result/' + str(index_binary_config_app_arg[0]) + '-' + index_binary_config_app_arg[3] + '/terminal.log'
  
  print("command: ", command)
  os.system(command)



if __name__ == "__main__":

  # STEP0 compile
  for index, binary, config, app, _ in experimentList:
    if binary[0] == "R":
      os.system('ISA=riscv CC=riscv64-linux-gnu-gcc make -C '+GEM5_DIR+'/myWorkDir/app/'+app)
    elif binary[0] == "X":
      os.system('ISA=X86 CC=x86_64-linux-gnu-gcc make -C '+GEM5_DIR+'/myWorkDir/app/'+app)
    else:
      assert(False)
    os.makedirs(GEM5_DIR + '/myWorkDir/result/' + str(index) + '-' + app, exist_ok=True)

  # STEP1 init the cluster or multiProcess
  if not RUN_MODE == "singleProc":
    client = initClient(RUN_MODE)


  # STEP2 mark start time
  startTime = time.time()

  # STEP3 run them
  if RUN_MODE == "singleProc":
    for i, index_binary_config_app_arg in enumerate(experimentList):
      runSimu(index_binary_config_app_arg)
      print("----------> Finish %d/%d Simu, After %f minutes" % \
        (i+1, len(experimentList), (time.time() - startTime)/60))

  else:
    futureList = []
    for index_binary_config_app_arg in experimentList:
      futureList.append(client.submit(runSimu, index_binary_config_app_arg))

    for i, future in enumerate(futureList):
      future.result()
      print("----------> Finish %d/%d Simu, After %f minutes" % \
        (i+1, len(experimentList), (time.time() - startTime)/60))

