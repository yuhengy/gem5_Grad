
instSimu = 100000000

GET_FROM_BUFFER = False

def getMiss_acc(fileName):
  finish = 0

  with open(fileName) as f:
    for line in f.readlines():
      words = line.split()

      if len(words) > 0 and words[0] == "system.l3.overall_misses::total":
        miss = int(words[1]) / instSimu * 1000
        finish += 1
      if len(words) > 0 and words[0] == "system.l3.overall_accesses::total":
        acc = int(words[1]) / instSimu * 1000
        finish += 1

      if finish == 2:
        return miss, acc

  print(fileName + " FAIL!!!", end="")
  return 0, 0


def getLLCMiss(sizeToBaseIndex, resultDir):

  # CASE1: From Buffer
  if GET_FROM_BUFFER:
    with open(resultDir + "/missRate.json",'r') as f:
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
      missList = [[], [], [], []]
      accList = [[], [], [], []]
      for weight in weightList:

        # deal with the 4 test of this SPEC now
        for k, j in enumerate(range(baseIndex+1000+SPECList[i][0], baseIndex+4001+SPECList[i][0], 1000)):
          miss, acc = getMiss_acc(resultDir + "/%d-SPEC2017/stats.txt"%j)
          if acc == 0:
            print(name, "is skiped")
            miss, acc = getMiss_acc(resultDir + "/%d-SPEC2017/stats.txt"%(j+1000))
            if miss==0 or acc==0:
              assert(False)
          missList[k].append(weight * miss)
          accList[k].append(weight * acc)
        i += 1

      for miss, acc in zip(missList, accList):
        result[name].append(sum(miss))
        result[name].append(sum(acc))

    result_all[size] = result

  print(result_all)
  with open(resultDir + "/missRate.json", "w") as f:
    import json
    json.dump(result_all, f)
  return result_all




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.plotScript.getResult myWorkDir/result\n")
    exit(-1)

  getLLCMiss({0:10000, 1:20000, 10:30000, 20:40000, 40:50000, 100:60000}, sys.argv[1])

