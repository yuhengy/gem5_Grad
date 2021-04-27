
import os

COMPILE_LIBM5 = False

os.system("scons -j9 build/X86/gem5.opt")

if COMPILE_LIBM5:
  os.system("scons -C util/m5/ -j9 build/x86/out/m5")
