
import os
import time


#----------------------
RUN_MODE = "multiProc" # singleProc, multiProc, cluster
NUM_PROC = 8

gem5Binary = 'gem5.debug'
experimentList = [[i, 'simple.py', 'hello'] for i in range(1)]
#----------------------


def initClient():
  from dask.distributed import Client, SSHCluster, progress

  # STEP1 create a cluster
  # NOTE: nthreads = 1 means each runsimu() use one thread
  #       nproces = -1 means auto set nproces = ncores / nthreads
  '''
  cluster = SSHCluster(
    ["myUbuntu", "myUbuntu"],
    connect_options=[{"username":"yuhengy"}, {"username":"yuhengy"}],
    scheduler_options={"idle_timeout":"10 seconds"},
    worker_options={"nthreads": 1, "nprocs": -1, "lifetime":"1 hour"},
    remote_python=["python3", "python3"]
  )
  '''
  cluster = SSHCluster(
    ["localhost", "localhost"],
    connect_options=[{"username":"vagrant"}, {"username":"vagrant"}],
    scheduler_options={"idle_timeout":"10 seconds"},
    worker_options={"nthreads": 1, "nprocs": -1, "lifetime":"1 hour"},
    remote_python=["python3", "python3"]
  )
  
  time.sleep(1)
  print(cluster)

  # STEP 2 setup a client
  client = Client(cluster)

  return client


def runSimu(index_config_app):
  if not os.path.exists(os.path.expanduser('~') + '/myMnt/gem5'):
    os.system("sshfs myMac:Documents/ProjectGraduation ~/myMnt")

  os.system( \
    '~/myMnt/gem5/build/RISCV/' + gem5Binary + \
    ' --outdir='+ os.path.expanduser('~') + '/myMnt/gem5/myWorkDir/result/' + str(index_config_app[0]) + '-' + index_config_app[1][:-3] + index_config_app[2] + \
    ' ~/myMnt/gem5/myWorkDir/config/' + index_config_app[1] + \
    ' -c ~/myMnt/gem5/myWorkDir/app/' + index_config_app[2] \
  )




if __name__ == "__main__":

  # STEP1 init the cluster or multiProcess
  if RUN_MODE == "multiProc":
    from concurrent.futures import ProcessPoolExecutor
    client = ProcessPoolExecutor(NUM_PROC)
  elif RUN_MODE == "cluster":
    client = initClient()


  # STEP2 mark start time
  startTime = time.time()

  # STEP3 run them
  if RUN_MODE == "singleProc":
    for i, index_config_app in enumerate(experimentList):
      runSimu(index_config_app)
      print("----------> Finish %d/%d Simu, After %f minutes" % \
        (i+1, len(experimentList), (time.time() - startTime)/60))

  else:
    futureList = []
    for index_config_app in experimentList:
      futureList.append(client.submit(runSimu, index_config_app))

    for i, future in enumerate(futureList):
      future.result()
      print("----------> Finish %d/%d Simu, After %f minutes" % \
        (i+1, len(experimentList), (time.time() - startTime)/60))




