
import os

os.system("scons -j9 build/RISCV/gem5.opt")
os.system("scons -j9 build/X86/gem5.opt")

os.system("scons -C util/m5/ -j9 build/riscv/out/m5")
os.system("scons -C util/m5/ -j9 build/X86/out/m5")
