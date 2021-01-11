
import sys
import os
import json
import shutil

if __name__ == "__main__":

  dataDir = 'myWorkDir/result'

  dirContent = [dataDir + "/" + x for x in os.listdir(dataDir)]
  for f in dirContent:
    try:
      os.remove(f)
    except:
      shutil.rmtree(f)
