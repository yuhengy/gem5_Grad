
import os
import time

#-------------------- 1/4 Run Config Begin --------------------
RUN_MODE = "slurmCluster" # singleProc, multiProc, slurmCluster

REDIRECT_TERMINAL_OUTPUT = True
COMPILE_APP = False
#-------------------- 1/4 Run Config End --------------------


#-------------------- 2/4 Base CPU Config Begin --------------------
runOpt = ' --cpu-type=DerivO3CPU  \
           --num-cpus=1 \
           --cacheline_size=256 \
           --caches --l1d_size=16kB --l1i_size=16kB \
           --l1d_assoc=4 --l1i_assoc=4 \
           --l2cache \
           --l2_size=128kB --l2_assoc=8 \
           --l3cache \
           --l3_size=4MB --l3_assoc=16 --l3_mshrs=%d \
           --mem-size=4GB' % (4*1024*1024 / 256 + 20)
#-------------------- 2/4 Base CPU Config End --------------------


#-------------------- 3/4 Security Config Begin --------------------
rekHOptBase = ' --l3reKeyHit --l3_max_evict_per_epoch=%d'
rekMOptBase = ' --l3reKeyMiss --l3_max_evict_per_epoch=%d'
rekMAOptBase = ' --l3reKeyMissAddr --l3_max_evict_per_epoch=%d'

secPara = [[10000, 2], [20000, 4*1024*1024 / 256 *1], [30000, 4*1024*1024 / 256 *2], [40000, 4*1024*1024 / 256 *3], [50000, 4*1024*1024 / 256 *4], [60000, 4*1024*1024 / 256 *6], [70000, 4*1024*1024 / 256 *8], [80000, 4*1024*1024 / 256 *12], [90000, 4*1024*1024 / 256 *20], [100000, 4*1024*1024 / 256 *40], [110000, 4*1024*1024 / 256 *100]]
#-------------------- 3/4 Security Config End --------------------


#-------------------- 4/4 experiment Config Begin --------------------
experimentList = []

## SEPT1 hello
#rstCktOpt = ' --checkpoint-restore=1 --maxinsts=50000000 --warmup-insts=1000000'
#experimentList.append([0, 'X86/gem5.opt', runOpt, 'hello', ''])
#experimentList.append([1, 'X86/gem5.opt', runOpt + rstCktOpt, 'hello', ''])
#experimentList.append([2, 'X86/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'hello', ''])
#experimentList.append([3, 'X86/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'hello', ''])

## STEP2 stream
#experimentList.append([20, 'X86/gem5.opt', runOpt, 'stream', ''])
#experimentList.append([21, 'X86/gem5.opt', runOpt + rstCktOpt, 'stream', ''])
#experimentList.append([22, 'X86/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'stream', ''])
#experimentList.append([23, 'X86/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'stream', ''])
#experimentList.append([24, 'X86/gem5.opt', runOpt + rstCktOpt + rekMAOpt, 'stream', ''])


for baseI, size in secPara:
  rekHOpt = rekHOptBase % size
  rekMOpt = rekMOptBase % size
  rekMAOpt = rekMAOptBase % max(2, int(size/4096))

  ## STEP3 docDist
  #experimentList.append([100, 'X86/gem5.opt', runOpt, 'docDist', ''])
  #experimentList.append([baseI+101, 'X86/gem5.opt', runOpt + rstCktOpt, 'docDist', ''])
  #experimentList.append([baseI+102, 'X86/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'docDist', ''])
  #experimentList.append([baseI+103, 'X86/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'docDist', ''])
  #experimentList.append([baseI+104, 'X86/gem5.opt', runOpt + rstCktOpt + rekMAOpt, 'docDist', ''])

  ## STEP4 mrsFast
  #arg = '--search myWorkDir/app/mrsFast/dataset/chr3_50K.fa --seq myWorkDir/app/mrsFast/dataset/chr3_50K_2000.fq'
  #experimentList.append([200, 'X86/gem5.opt', runOpt, 'mrsFast', arg])
  #experimentList.append([baseI+201, 'X86/gem5.opt', runOpt + rstCktOpt, 'mrsFast', arg])
  #experimentList.append([baseI+202, 'X86/gem5.opt', runOpt + rstCktOpt + rekHOpt, 'mrsFast', arg])
  #experimentList.append([baseI+203, 'X86/gem5.opt', runOpt + rstCktOpt + rekMOpt, 'mrsFast', arg])
  #experimentList.append([baseI+204, 'X86/gem5.opt', runOpt + rstCktOpt + rekMAOpt, 'mrsFast', arg])

  ## STEP5 SPEC2017
  SPECOpt = ' --benchmark=%s --simpt-ckpt=%d \
              --checkpoint-restore=1 --at-instruction \
              --maxinsts=100000000 --warmup-insts=20000000'
  from SPECList import SPECList
  #SPECList = []
  #SPECList = [[0, "blender_r", 0]]

  for i, name, simptID in SPECList:
    experimentList.append([baseI+i+1000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID), 'SPEC2017', ''])
    experimentList.append([baseI+i+2000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID) + rekHOpt, 'SPEC2017', ''])
    experimentList.append([baseI+i+3000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID) + rekMOpt, 'SPEC2017', ''])
    experimentList.append([baseI+i+4000, 'X86/gem5.opt', runOpt + SPECOpt%(name,simptID) + rekMAOpt, 'SPEC2017', ''])

print("Number of experiments: ", len(experimentList))
#-------------------- 4/4 Run Config Begin --------------------


def initClient(RUN_MODE):
  from dask.distributed import Client, LocalCluster

  # STEP1 choose a cluster
  if RUN_MODE == "multiProc":
    cluster = LocalCluster(threads_per_worker=1, local_directory="/tmp")
  
  elif RUN_MODE == "slurmCluster":
    from dask_jobqueue import SLURMCluster

    cluster = SLURMCluster(cores=64, processes=64, memory="250G", interface="ib0", walltime="24:00:00", local_directory="/tmp")
    #cluster.adapt(minimum_jobs=1, maximum_jobs=2, wait_count=100)
    cluster.scale(jobs=6)
  
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
    command += ' > ' + GEM5_DIR + '/myWorkDir/result/' + str(index_binary_config_app_arg[0]) + '-' + index_binary_config_app_arg[3] + '/terminal.log 2>&1'
  
  print("command: ", command)
  os.system(command)



if __name__ == "__main__":
  GEM5_DIR = os.getcwd()

  # STEP0 compile
  for index, binary, config, app, _ in experimentList:
    os.makedirs(GEM5_DIR + '/myWorkDir/result/' + str(index) + '-' + app, exist_ok=True)
      
    if COMPILE_APP:
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

