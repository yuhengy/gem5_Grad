

def getIPC(fileName):
  with open(fileName) as f:
    for line in f.readlines():
      words = line.split()
      if len(words) > 0 and words[0] == "system.switch_cpus.ipc":
        return float(words[1])

  print(fileName + " FAIL!!!", end="")
  return 0


def getResult(sizeToBaseIndex, resultDir):
  result_all = dict()

  for size, baseIndex in sizeToBaseIndex.items():
    result = dict()

    # STEP1 docDist
    #result["docDist"] = []
    #for i in range(baseIndex+101, baseIndex+105):
    #  result["docDist"].append(getIPC(resultDir + "/%d-docDist/stats.txt"%i))

    # STEP2 mrsFast
    #result["mrsFast"] = []
    #for i in range(baseIndex+201, baseIndex+205):
    #  result["mrsFast"].append(getIPC(resultDir + "/%d-mrsFast/stats.txt"%i))

    # STEP3 SPEC
    from ..runScript.SPECList import SPECList, SPEC_name, SPEC_simptNum, SPEC_weight
    i = 0

    for name, weightList in zip(SPEC_name, SPEC_weight):

      # deal with one SPEC now
      result[name] = []
      IPCList = [[], [], [], []]
      for weight in weightList:

        # deal with the 4 test of this SPEC now
        for k, j in enumerate(range(baseIndex+1000+SPECList[i][0], baseIndex+4001+SPECList[i][0], 1000)):
          IPC = getIPC(resultDir + "/%d-SPEC2017/stats.txt"%j)
          if IPC == 0:
            print(name)
          IPCList[k].append(weight * IPC)
        i += 1

      for IPC in IPCList:
        result[name].append(sum(IPC))

    result_all[size] = result

  print(result_all)
  with open(resultDir + "/summary.json", "w") as f:
    import json
    json.dump(result_all, f)
  return result_all




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.plotScript.plot4Config myWorkDir/result\n")
    exit(-1)

  getResult({0:10000, 1:20000, 10:30000, 20:40000, 40:50000, 100:60000}, sys.argv[1])

