

SPEC_name = ["blender_r"  , "bwaves_r"   , "cactuBSSN_r", "cam4_r"     , \
             "deepsjeng_r", "exchange2_r", "fotonik3d_r", "gcc_r"      , \
             "lbm_r"      , "leela_r"    , "mcf_r"      , "nab_r"      , \
             "namd_r"     , "omnetpp_r"  , "parest_r"   , "perlbench_r", \
             "povray_r"   , "roms_r"     , "wrf_r"      , "x264_r"     , \
             "xalancbmk_r", "xz_r"]

SPEC_simptNum = [9 , 8 , 9 , 7, \
                 7 , 7 , 9 , 9, \
                 8 , 7 , 8 , 7, \
                 9 , 5 , 7 , 7, \
                 8 , 10, 10, 8, \
                 7 , 8]

SPEC_weight = [[0.0275665, 0.0741232, 0.020343, 0.12872, 0.104089, 0.387335, 0.241743, 0.00329266, 0.0127878], \
               [0.0129522, 0.0610822, 0.0118409, 0.0281269, 0.463136, 0.0643777, 0.309779, 0.0487048],\
               [0.0263519, 0.0159049, 0.0118533, 0.122016, 0.00981082, 0.00348234, 0.257526, 0.118801, 0.434254],\
               [0.035832, 0.126088, 0.0036612, 0.0434091, 0.179812, 0.0426609, 0.568536],\
               [0.192761, 0.193841, 0.18793, 0.106367, 0.241775, 0.0766511, 0.000674746],\
               [0.292077, 0.0390213, 0.0816812, 0.0207235, 0.184109, 0.23295, 0.149438],\
               [0.150917, 0.246895, 0.0465371, 0.0297889, 0.0620251, 0.138022, 0.0804902, 0.198312, 0.047012],\
               [0.003854, 0.0652913, 0.513262, 0.0238041, 0.00181365, 0.126502, 0.0181365, 0.0818409, 0.165495],\
               [0.0179227, 0.00132217, 0.171853, 0.0783311, 0.00290877, 0.621772, 0.105803, 8.81446e-05],\
               [0.376448, 0.0487234, 0.131293, 0.0145521, 0.0138375, 0.31824, 0.0969055],\
               [0.23595, 0.107878, 0.0345005, 0.0836766, 0.0961086, 0.0201192, 0.0361557, 0.385611],\
               [0.327582, 0.0739881, 0.0979208, 0.00683477, 0.174497, 0.0698076, 0.24937],\
               [0.0828497, 0.0577172, 0.166451, 0.0623095, 0.0814512, 0.14733, 0.203732, 0.126811, 0.0713481],\
               [0.151811, 0.00512175, 0.419265, 0.000628987, 0.423174],\
               [0.0628719, 0.412752, 0.0666975, 0.0174644, 0.271632, 0.0829422, 0.0856404],\
               [0.258849, 0.0415677, 0.093751, 0.099892, 0.261194, 0.107206, 0.137541],\
               [0.0199318, 0.0923221, 0.233611, 0.114129, 0.0715615, 0.0884906, 0.184576, 0.195378],\
               [0.0253134, 0.0684942, 0.106838, 0.0790428, 0.0613823, 0.0778814, 0.154315, 0.115239, 0.0395532, 0.27194],\
               [0.129819, 0.175323, 0.0648202, 0.0372811, 0.181314, 0.101274, 0.0307446, 0.0737765, 0.0232758, 0.182372],\
               [0.0802096, 0.0546884, 0.0901219, 0.0772474, 0.191181, 0.105617, 0.193118, 0.207816],\
               [0.23983, 0.230914, 0.0840156, 0.0291483, 0.131724, 0.0539672, 0.2304],\
               [0.000536423, 0.341702, 0.00343311, 0.336015, 0.044845, 0.00504238, 0.158352, 0.110074]]


# NOTE: These are fail SPEC: bwaves_r, cactuBSSN_r, cam4_r, gcc_r, mcf_r, omnetpp_r, perlbench_r, roms_r, xalancbmk_r
SPEC_failName = ["bwaves_r", "cam4_r", "gcc_r", "omnetpp_r", "perlbench_r", "povray_r", "roms_r", "xalancbmk_r", "deepsjeng_r", "exchange2_r", "leela_r", "namd_r", "x264_r"]
SPEC_failIndex = sorted([SPEC_name.index(failName) for failName in SPEC_failName], reverse = True)
for failIndex in SPEC_failIndex:
  del(SPEC_name[failIndex])
  del(SPEC_simptNum[failIndex])
  del(SPEC_weight[failIndex])


SPECList = []
i = 0
for j, name in enumerate(SPEC_name):
  for simptID in range(SPEC_simptNum[j]):
    SPECList.append([i, name, simptID])
    i += 1




if __name__ == "__main__":

  ## Obtain dataDir location
  import sys
  if (len(sys.argv) < 2):
    print("Usage: python3 -m myWorkDir.runScript.SPECList myWorkDir/app/SPEC2017\n")
    exit(-1)

  readWeight = []
  for name in SPEC_name:
    readWeight.append([])
    with open(sys.argv[1] + "/ckpt/" + name + "/results.weights") as f:
      for line in f.readlines():
        readWeight[-1].append(float(line.split()[0]))

  print(readWeight)

