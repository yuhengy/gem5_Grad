 

# This is get from CaSA
from .plotBaseTradeoff import accToLeak, geo_mean
import math

def plotMyTradeoff(result):

  # STEP1 set epoch size list
  sizeList = [1,2,3,4,6,8,12,20,40,100]

  xToPlot1 = [[],[],[]]
  xToPlot2 = [[],[],[]]
  yToPlot = []
  for size in sizeList:
    IPCNotSecu_all = [i[0] for i in list(result[size].values())]
    IPCSecu_all1 = [i[1] for i in list(result[size].values())]
    IPCSecu_all2 = [i[2] for i in list(result[size].values())]
    IPCSecu_all3 = [i[3] for i in list(result[size].values())]
    xToPlot1[0].append(geo_mean(IPCSecu_all1)/geo_mean(IPCNotSecu_all) - 1)
    xToPlot1[1].append(geo_mean(IPCSecu_all2)/geo_mean(IPCNotSecu_all) - 1)
    xToPlot1[2].append(geo_mean(IPCSecu_all3)/geo_mean(IPCNotSecu_all) - 1)
    xToPlot2[0].append(result[size]["parest_r"][1]/result[size]["parest_r"][0] - 1)
    xToPlot2[1].append(result[size]["parest_r"][2]/result[size]["parest_r"][0] - 1)
    xToPlot2[2].append(result[size]["parest_r"][3]/result[size]["parest_r"][0] - 1)
    yToPlot.append(accToLeak[size])


  print("xToPlot1:", xToPlot1)
  print("xToPlot2:", xToPlot2)
  print("yToPlot:", yToPlot)
  yToPlot[1] += 15


  # STEP2: plot them
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=(6.4, 5.6))

  ax1 = plt.subplot2grid((7,1), (0,0), rowspan=3 )
  ax2 = plt.subplot2grid((7,1), (4,0), rowspan=3)


  ax1.plot(xToPlot1[0], yToPlot, color='blue', marker="o", label="LLC Access")
  ax1.plot(xToPlot1[1], yToPlot, color='green', marker="o", linestyle="--", label="LLC Miss")
  ax1.plot(xToPlot1[2], yToPlot, color='red', marker="o", linestyle=":", label="Max LLC Miss for Each Address")

  ax2.plot(xToPlot2[0], yToPlot, color='blue', marker="o", label="Count LLC Access")
  ax2.plot(xToPlot2[1], yToPlot, color='green', marker="o", linestyle="--", label="Count LLC Miss")
  ax2.plot(xToPlot2[2], yToPlot, color='red', marker="o", linestyle=":", label="Count Max LLC Miss for Each Address")




  ax1.set_ylabel("# of Seconds to Leak 1 bit                    ", color='black', fontsize=12, loc="top")
  ax1.legend(prop = {'size':10}, bbox_to_anchor=(1.015, 1.21), ncol=3)
  ax1.set_xlabel("Performance Overhead", fontsize=12)
  ax2.set_xlabel("Performance Overhead", fontsize=12)

  ax1.set_xticks([-0.4, -0.3, -0.2, -0.1, 0])
  ax1.set_xticklabels(["40%", "30%", "20%", "10%", "0%"])
  ax2.set_xticks([-0.4, -0.3, -0.2, -0.1, 0])
  ax2.set_xticklabels(["40%", "30%", "20%", "10%", "0%"])


  ax1.set_title("(a) geomean", fontsize=12, fontweight="bold", y = -0.38)
  ax2.set_title("(b) parest_r", fontsize=12, fontweight="bold", y = -0.38)

  plt.savefig("myTradeoff.pdf", bbox_inches="tight")
  plt.cla()




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.plotScript.plotMyTradeoff myWorkDir/result\n")
    exit(-1)
  resultDir = sys.argv[1]

  from .getResult import getResult
  #result = getResult({1:10000, 10:20000, 40:30000, 200:40000, 1000:50000, 4000:60000, 20000:70000, 100000:80000}, resultDir)
  result = getResult({0:10000, 1:20000, 2:30000, 3:40000, 4:50000, 6:60000, 8:70000, 12:80000, 20:90000, 40:100000, 100:110000}, resultDir)

  plotMyTradeoff(result)





