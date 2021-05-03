

GET_FROM_BUFFER = False

def getCPI(fileName):
  with open(fileName) as f:
    for line in f.readlines():
      words = line.split()
      if len(words) > 0 and words[0] == "system.switch_cpus.cpi":
        return float(words[1])

  print(fileName + " FAIL!!!", end="")
  return 0


def getResult(sizeToBaseIndex, resultDir):

  # CASE1: From Buffer
  if GET_FROM_BUFFER:
    with open(resultDir + "/summary.json",'r') as f:
      import json
      result = json.load(f, object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
    return result


  # CASE2: Compute
  result_all = dict()

  for size, baseIndex in sizeToBaseIndex.items():
    result = dict()

    # STEP3 SPEC
    from ..runScript.SPECList import SPECList, SPEC_name, SPEC_simptNum, SPEC_weight
    i = 0

    for name, weightList in zip(SPEC_name, SPEC_weight):

      # deal with one SPEC now
      result[name] = []
      CPIList = [[], [], [], []]
      for weight in weightList:

        # deal with the 4 test of this SPEC now
        for k, j in enumerate(range(baseIndex+1000+SPECList[i][0], baseIndex+4001+SPECList[i][0], 1000)):
          CPI = getCPI(resultDir + "/%d-SPEC2017/stats.txt"%j)
          if CPI == 0:
            print(name, "is skiped")
            CPI = getCPI(resultDir + "/%d-SPEC2017/stats.txt"%(j+1000))
            if CPI == 0:
              assert(False)
          CPIList[k].append(weight * CPI)
        i += 1

      for CPI in CPIList:
        result[name].append(1 / sum(CPI))

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
    print("Usage: python3 -m myWorkDir.plotScript.getResult myWorkDir/result\n")
    exit(-1)

  getResult({0:10000, 1:20000, 10:30000, 20:40000, 40:50000, 100:60000}, sys.argv[1])

