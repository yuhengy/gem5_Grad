

def geo_mean(iterable):
  import numpy as np
  a = np.array(iterable)
  return a.prod()**(1.0/len(a))


def plotBaseSlowdown(result):

  # STEP1 get insteresting data
  sizeList = [0, 4, 40]
  #sizeList = [1, 1, 1]

  xToPlot = sorted(list(result[sizeList[0]].keys())) + ["geomean"]
  yToPlot = [[], [], [], [], [], [], [], []]

  for name in xToPlot[:-1]:
    yToPlot[0].append(result[sizeList[0]][name][2])
    yToPlot[1].append(result[sizeList[0]][name][3] - result[sizeList[0]][name][2])
    yToPlot[2].append(result[sizeList[1]][name][2])
    yToPlot[3].append(result[sizeList[1]][name][3] - result[sizeList[1]][name][2])
    yToPlot[4].append(result[sizeList[2]][name][2])
    yToPlot[5].append(result[sizeList[2]][name][3] - result[sizeList[2]][name][2])
    yToPlot[6].append(result[sizeList[0]][name][0])
    yToPlot[7].append(result[sizeList[0]][name][1] - result[sizeList[0]][name][0])

  for i in range(8):
    yToPlot[i].append(geo_mean(yToPlot[i]))

  print("xToPlot:", xToPlot)
  print("yToPlot:", yToPlot)

  for i in [1,3,5,7]:
    for j in range (len(yToPlot[0])):
      #assert((yToPlot[i-1][j]+yToPlot[i][j]) < 25 or yToPlot[i][j] > 65)
      if yToPlot[i][j] > 65:
        yToPlot[i][j] -= 40
      if yToPlot[i-1][j] > 65:
        yToPlot[i-1][j] -= 40


  # STEP2: plot them
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=(13, 3))
  ax = plt.subplot()

  offset = 0.18
  plt.rcParams['hatch.color'] = 'white'
  ax.bar([i-1.5*offset for i in range(len(xToPlot))], yToPlot[1], offset, color="black", alpha=0.2)
  ax.bar([i-1.5*offset for i in range(len(xToPlot))], yToPlot[0], offset, bottom=yToPlot[1], color="black", hatch="xxxxx", alpha=0.2)
  ax.bar([i-0.5*offset for i in range(len(xToPlot))], yToPlot[3], offset, color="black", alpha=0.5)
  ax.bar([i-0.5*offset for i in range(len(xToPlot))], yToPlot[2], offset, bottom=yToPlot[3], color="black", hatch="xxxxx", alpha=0.5)
  ax.bar([i+0.5*offset for i in range(len(xToPlot))], yToPlot[5], offset, color="black", alpha=0.7)
  ax.bar([i+0.5*offset for i in range(len(xToPlot))], yToPlot[4], offset, bottom=yToPlot[5], color="black", hatch="xxxxx", alpha=0.8)
  ax.bar([i+1.5*offset for i in range(len(xToPlot))], yToPlot[7], offset, color="black", alpha=1)
  ax.bar([i+1.5*offset for i in range(len(xToPlot))], yToPlot[6], offset, bottom=yToPlot[7], color="black", hatch="xxxxx", alpha=1)


  label1 = ax.bar(0, 0, label="Epoch Size = 1 LLC Access", color="black", alpha=0.2)
  label2 = ax.bar(0, 0, label="Epoch Size = 4 Units", color="black", alpha=0.5)
  label3 = ax.bar(0, 0, label="Epoch Size = 40 Units", color="black", alpha=0.7)
  label4 = ax.bar(0, 0, label="Epoch Size = Infinite", color="black", alpha=1)
  ax.add_artist(ax.legend(handles=(label1, label2, label3, label4), bbox_to_anchor=(1, 1.18), ncol=4, prop={'size':11 }))

  label1 = ax.bar(0, 0, label="LLC Miss", hatch="xxxxx", color="black", alpha=1)
  label2 = ax.bar(0, 0, label="LLC Hit", color="black", alpha=1)
  ax.add_artist(ax.legend(handles=(label1, label2), bbox_to_anchor=(1, 1.32), ncol=2, prop={'size':11 }))


  ax.set_ylabel("LLC Accesses\nper 1000 Instructions", color='black', fontsize=16)
  #ax.set_yscale("log")
  #ax.set_ylim(0.5, 1.1)

  #ax.set_yticks([1,2,4,8,16,32,64])
  #ax.set_yticklabels([1,2,4,8,16,32,64])

  ax.set_yticks([5,15,23.5,26.5,35])
  ax.set_yticklabels([5,15,25,65,75])
  ax.axhline(y=25, color="white",lw=12)
  ax.axhline(y=26.5, color="black",lw=1, linestyle="--")
  ax.axhline(y=23.5, color="black",lw=1, linestyle="--")
  plt.text(-0.95, 27, '__')
  plt.text(-0.93, 24.8, ' ', bbox=dict(facecolor='white', edgecolor='white'), fontsize=3)
  plt.text(-0.95, 24, '__')
  plt.text(9.78, 27, '__')
  plt.text(9.78, 24.8, ' ', bbox=dict(facecolor='white', edgecolor='white'), fontsize=3)
  plt.text(9.78, 24, '__')

  plt.yticks(fontsize=16)
  plt.xticks(fontsize=12)
  ax.set_xticks(range(len(xToPlot)))
  ax.set_xticklabels(xToPlot, rotation=90)


  plt.savefig("LLCMiss.pdf", bbox_inches="tight")
  plt.cla()




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.plotScript.plotBaseSlowdown myWorkDir/result\n")
    exit(-1)
  resultDir = sys.argv[1]

  from .getLLCMiss import getLLCMiss
  result = getLLCMiss({0:10000, 1:20000, 2:30000, 3:40000, 4:50000, 6:60000, 8:70000, 12:80000, 20:90000, 40:100000, 100:110000}, resultDir)
  #result = getLLCMiss({1:20000}, resultDir)

  plotBaseSlowdown(result)

