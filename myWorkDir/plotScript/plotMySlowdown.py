

def geo_mean(iterable):
  import numpy as np
  a = np.array(iterable)
  return a.prod()**(1.0/len(a))


def plotMySlowdown(result):

  # STEP1 get insteresting data
  size = 4
  #size = 1

  xToPlot = [[],[],[]]
  yToPlot = [[],[],[]]
  raw = result[size]

  xToPlot[0] = sorted(list(raw.keys())) + ["geomean"]
  xToPlot[1] = sorted(list(raw.keys())) + ["geomean"]
  xToPlot[2] = sorted(list(raw.keys())) + ["geomean"]

  for name in xToPlot[0][:-1]:
    yToPlot[0].append(min(1, raw[name][1] / raw[name][0]))
    yToPlot[1].append(min(1, raw[name][2] / raw[name][0]))
    yToPlot[2].append(min(1, raw[name][3] / raw[name][0]))

  yToPlot[0].append(geo_mean(yToPlot[0]))
  yToPlot[1].append(geo_mean(yToPlot[1]))
  yToPlot[2].append(geo_mean(yToPlot[2]))

  print("xToPlot:", xToPlot)
  print("yToPlot:", yToPlot)


  # STEP2: plot them
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=(13, 3))
  ax = plt.subplot()
  plt.rc('font', size=16)

  offset = 0.18
  ax.bar([i-1.5*offset for i in range(len(xToPlot[0]))], yToPlot[0], offset, color="black", alpha=0.2, label="Count LLC Access")
  ax.bar([i-0.5*offset for i in range(len(xToPlot[1]))], yToPlot[1], offset, color="black", alpha=0.5, label="Count LLC Miss")
  ax.bar([i+0.5*offset for i in range(len(xToPlot[2]))], yToPlot[2], offset, color="black", alpha=0.7, label="Count Max LLC Miss for Each Address")
  ax.bar([i+1.5*offset for i in range(len(xToPlot[2]))], [1] * len(yToPlot[2]), offset, color="black", alpha=1  , label="Epoch Size = Infitie")
  for binID, IPC in enumerate(yToPlot[0]):
    ax.text(binID-1.5*offset, IPC + 0.01, "%.2f"%IPC, ha='center', rotation=90, fontsize=11)
  for binID, IPC in enumerate(yToPlot[1]):
    ax.text(binID-0.5*offset, IPC + 0.01, "%.2f"%IPC, ha='center', rotation=90, fontsize=11)
  for binID, IPC in enumerate(yToPlot[2]):
    ax.text(binID+0.5*offset, IPC + 0.01, "%.2f"%IPC, ha='center', rotation=90, fontsize=11)
  for binID, IPC in enumerate(yToPlot[2]):
    ax.text(binID+1.5*offset, 1 + 0.01, "%.2f"%1, ha='center', rotation=90, fontsize=11)

  ax.set_ylabel("Normalized IPC", color='black', fontsize=16)
  ax.set_ylim(0.7, 1.1)

  ax.set_xticks(range(len(xToPlot[0])))
  ax.set_xticklabels(xToPlot[0], rotation=90)
  plt.yticks(fontsize=16)
  plt.xticks(fontsize=12)
  ax.legend(ncol=4, bbox_to_anchor=(1, 1.2), prop = {'size':11})


  plt.savefig("mySlowdown.pdf", bbox_inches="tight")
  plt.cla()




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.plotScript.plotMySlowdown myWorkDir/result\n")
    exit(-1)
  resultDir = sys.argv[1]

  from .getResult import getResult
  result = getResult({0:10000, 1:20000, 2:30000, 3:40000, 4:50000, 6:60000, 8:70000, 12:80000, 20:90000, 40:100000, 100:110000}, resultDir)
  #result = getResult({1:20000}, resultDir)

  plotMySlowdown(result)

