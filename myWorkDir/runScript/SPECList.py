

SPECList = []

info_all = [["blender_r", 9]  , ["bwaves_r", 8]   , ["cactuBSSN_r", 9], ["cam4_r", 7]     , \
            ["deepsjeng_r", 7], ["exchange2_r", 7], ["fotonik3d_r", 9], ["gcc_r", 9]      , \
            ["lbm_r", 8]      , ["leela_r", 7]    , ["mcf_r", 8]      , ["nab_r", 7]      , \
            ["namd_r", 9]     , ["omnetpp_r", 5]  , ["parest_r", 7]   , ["perlbench_r", 7], \
            ["povray_r", 8]   , ["roms_r", 10]    , ["wrf_r", 10]     , ["x264_r", 8]     , \
            ["xalancbmk_r", 7], ["xz_r", 8]]

i = 0
for name, simptNum in info_all:
  for simptID in range(simptNum):
    SPECList.append([i, name, simptID])
    i += 1

