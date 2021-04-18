
import os
import time

#-------------------- 1/3 Run Config Begin --------------------
RUN_MODE = "singleProc" # singleProc, multiProc

REDIRECT_TERMINAL_OUTPUT = False
#-------------------- 1/3 Run Config End --------------------


#-------------------- 2/3 Run Config Begin --------------------
runOpt = ' --cpu-type=DerivO3CPU  \
           --num-cpus=1 \
           --caches --l1d_size=32kB --l1i_size=32kB \
           --l1d_assoc=8 --l1i_assoc=8 \
           --l2cache \
           --l2_size=512kB --l2_assoc=16 \
           --l3cache \
           --l3_size=2MB --l3_assoc=16 --l3_mshrs=%d \
           --mem-size=4GB' % (2*1024*1024 / 64 + 20)

#rekHOpt = ' --l3reKeyHit --l3_max_evict_per_epoch=%d' % (2*1024*1024 / 64 * 100)
rekHOpt = ' --l3reKeyHit --l3_max_evict_per_epoch=%d' % (2)
#rekMOpt = ' --l3reKeyMiss --l3_max_evict_per_epoch=%d' % (2*1024*1024 / 64 * 100)
rekMOpt = ' --l3reKeyMiss --l3_max_evict_per_epoch=%d' % (2)
#rekMAOpt = ' --l3reKeyMissAddr --l3_max_evict_per_epoch=%d' % (2*1024*1024 / 64 * 100)
rekMAOpt = ' --l3reKeyMissAddr --l3_max_evict_per_epoch=%d' % (2)
#-------------------- 2/3 Run Config End --------------------


#-------------------- 3/3 Run Config Begin --------------------
experimentList = []

## SEPT1 hello
rstCktOpt = ' --checkpoint-restore=1 --maxinsts=50000000 --warmup-insts=1000000'
#experimentList.append([0, 'X86/gem5.opt', runOpt, 'hello', ''])
#experimentList.append([1, 'X86/gem5.opt', runOpt + rstCktOpt, 'hello', ''])
#experimentList.append([2, 'X86/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'hello', ''])
#experimentList.append([3, 'X86/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'hello', ''])
#experimentList.append([10, 'RISCV/gem5.opt', runOpt, 'hello', ''])
#experimentList.append([11, 'RISCV/gem5.opt', runOpt + rstCktOpt, 'hello', ''])
#experimentList.append([12, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'hello', ''])
#experimentList.append([13, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'hello', ''])

## STEP2 stream
#experimentList.append([20, 'RISCV/gem5.opt', runOpt, 'stream', ''])
#experimentList.append([21, 'RISCV/gem5.opt', runOpt + rstCktOpt, 'stream', ''])
#experimentList.append([22, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'stream', ''])
#experimentList.append([23, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'stream', ''])
#experimentList.append([24, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMAOpt, 'stream', ''])

## STEP3 docDist
#experimentList.append([100, 'RISCV/gem5.opt', runOpt, 'docDist', ''])
#experimentList.append([101, 'RISCV/gem5.opt', runOpt + rstCktOpt, 'docDist', ''])
#experimentList.append([102, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'docDist', ''])
#experimentList.append([103, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'docDist', ''])
#experimentList.append([104, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMAOpt, 'docDist', ''])

## STEP4 mrsFast
arg = '--search myWorkDir/app/mrsFast/dataset/chr3_50K.fa --seq myWorkDir/app/mrsFast/dataset/chr3_50K_2000.fq'
experimentList.append([200, 'RISCV/gem5.opt', runOpt, 'mrsFast', arg])
#experimentList.append([201, 'RISCV/gem5.opt', runOpt + rstCktOpt, 'mrsFast', arg])
#experimentList.append([202, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'mrsFast', arg])
#experimentList.append([203, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'mrsFast', arg])
#experimentList.append([204, 'RISCV/gem5.opt', runOpt + rstCktOpt + rekMAOpt, 'mrsFast', arg])

## STEP5 SPEC2017
SPECOpt = ' --benchmark=%s --simpt-ckpt=%d \
            --checkpoint-restore=1 --at-instruction \
            --maxinsts=50000000 --warmup-insts=1000000'
from SPECList import SPECList
#SPECList = []
SPECList = [[0, "blender_r", 0]]

for i, name, simptID in SPECList:
  experimentList.append([i+1000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID), 'SPEC2017', ''])
  experimentList.append([i+2000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID) + rekHOpt, 'SPEC2017', ''])
  experimentList.append([i+3000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID) + rekMOpt, 'SPEC2017', ''])
  experimentList.append([i+4000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID) + rekMAOpt, 'SPEC2017', ''])

#-------------------- 3/3 Run Config Begin --------------------


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

  if index_binary_config_app_arg[3][:4] == 'SPEC':
    runShell = ''
  else:
    runShell = ' -c ' + GEM5_DIR + '/myWorkDir/app/' + index_binary_config_app_arg[3] + '/build/' + index_binary_config_app_arg[3] + ' --options="' + index_binary_config_app_arg[4] +'"'

  command = GEM5_DIR + '/build/' + index_binary_config_app_arg[1] + \
    ' --outdir='+ GEM5_DIR + '/myWorkDir/result/' + str(index_binary_config_app_arg[0]) + '-' + index_binary_config_app_arg[3] + \
    ' ' + GEM5_DIR + '/configs/example/se.py' + index_binary_config_app_arg[2] + \
    ' --checkpoint-dir=' + GEM5_DIR + '/myWorkDir/app/' + index_binary_config_app_arg[3] + \
    runShell

  if REDIRECT_TERMINAL_OUTPUT:
    command += ' > ' + GEM5_DIR + '/myWorkDir/result/' + str(index_binary_config_app_arg[0]) + '-' + index_binary_config_app_arg[3] + '/terminal.log'
  
  print("command: ", command)
  os.system(command)



if __name__ == "__main__":
  GEM5_DIR = os.getcwd()

  # STEP0 compile
  for index, binary, config, app, _ in experimentList:
    os.makedirs(GEM5_DIR + '/myWorkDir/result/' + str(index) + '-' + app, exist_ok=True)
    
    if app == 'SPEC2017':
      continue

    if binary[0] == "R":
      os.system('ISA=riscv CCPRE=riscv64-linux-gnu- make -C '+GEM5_DIR+'/myWorkDir/app/'+app)
    elif binary[0] == "X":
      os.system('ISA=X86 CCPRE=x86_64-linux-gnu- make -C '+GEM5_DIR+'/myWorkDir/app/'+app)
    else:
      assert(False)

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

