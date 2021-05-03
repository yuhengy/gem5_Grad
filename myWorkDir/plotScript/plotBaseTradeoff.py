

# This is get from CaSA
accToLeak_raw = [0, 964231168, 577044480, 502382592, 669843456, 507002880, 339345408, 395902976, 452460544, 383090688, 363560960, 311066624, 339345408, 367624192, 297959424, 319242240, 290979840, 280477696, 296976384, 269582336, 246415360, 254607360, 266731520, 252854272, 246939648, 257228800, 213843968, 222068736, 230293504, 226639872, 231505920, 216367104, 197132288, 203292672, 209453056, 205291520, 211156992, 182468608, 181174272, 185942016, 188088320, 192118784, 196804608, 176832512, 167968768, 171786240, 173342720, 177111040, 180879360, 170999808, 158924800, 162103296, 163577856, 166723584, 169869312, 160399360, 153223168, 155025408, 149192704, 151764992, 148439040, 138919936, 141197312, 143474688, 139460608, 133120000, 135168000, 132825088, 123666432, 125485056, 127303680, 129122304, 123863040, 120799232, 122454016, 114278400, 115802112, 117325824, 115015680, 116490240, 114032640, 115458048, 107479040, 108789760, 110100480, 110018560, 109903872, 108331008, 100925440, 102072320, 103219200, 104366080, 105512960, 102088704, 103186432, 96501760, 97517568, 98533376, 99549184, 100564992, 100564992]

accToLeak = [accToLeak_raw[0], accToLeak_raw[1]]
for i in range(2,99):
  accToLeak.append(sum(accToLeak_raw[i-2:i+3])/5)
accToLeak += [accToLeak_raw[99], accToLeak_raw[100]]

for i in range(len(accToLeak)):
  accToLeak[i] *= (4+12+43+100) / 2.4e9


def geo_mean(iterable):
  import numpy as np
  a = np.array(iterable)
  return a.prod()**(1.0/len(a))


def plotBaseTradeoff(result):

  # STEP1 set epoch size list
  sizeList = [1,2,3,4,6,8,12,20,40,100]

  xToPlot = [[],[]]
  yToPlot = []
  for size in sizeList:
    IPCNotSecu_all = [i[0] for i in list(result[size].values())]
    IPCSecu_all = [i[1] for i in list(result[size].values())]
    xToPlot[0].append(geo_mean(IPCSecu_all)/geo_mean(IPCNotSecu_all) - 1)
    xToPlot[1].append(result[size]["parest_r"][1]/result[size]["parest_r"][0] - 1)
    yToPlot.append(accToLeak[size])

  print("xToPlot:", xToPlot)
  print("yToPlot:", yToPlot)
  yToPlot[1] += 15


  # STEP2: plot them
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=(6.4, 2.8))
  ax = plt.subplot()

  #ax.plot(xToPlot[0], yToPlot, color='black', marker="o")
  ax.plot(xToPlot[0], yToPlot, color='blue', marker="o", label="geomean")
  ax.plot(xToPlot[1], yToPlot, color='green', marker="o", linestyle=":", label="parest_r")

  ax.set_ylabel("# of Seconds to Leak 1 bit", color='black', fontsize=12)
  ax.set_xlabel("Performance Overhead", fontsize=12)
  ax.legend(prop = {'size':12})

  ax.set_xticks([-0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0])
  ax.set_xticklabels(["35%", "30%", "25%", "20%", "15%", "10%", "5%", "0%"])

  plt.savefig("baseTradeoff.pdf", bbox_inches="tight")
  plt.cla()




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.plotScript.plotBaseTradeoff myWorkDir/result\n")
    exit(-1)
  resultDir = sys.argv[1]

  from .getResult import getResult
  #result = getResult({1:10000, 10:20000, 40:30000, 200:40000, 1000:50000, 4000:60000, 20000:70000, 100000:80000}, resultDir)
  result = getResult({0:10000, 1:20000, 2:30000, 3:40000, 4:50000, 6:60000, 8:70000, 12:80000, 20:90000, 40:100000, 100:110000}, resultDir)

  plotBaseTradeoff(result)

