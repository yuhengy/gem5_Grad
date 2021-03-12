
# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *
# import the caches which we made
from caches import *


def configSystem():
  # create the system we are going to simulate
  system = System()

  # Set the clock fequency of the system (and all of its children)
  system.clk_domain = SrcClockDomain()
  system.clk_domain.clock = '1GHz'
  system.clk_domain.voltage_domain = VoltageDomain()

  # Set up the system
  system.mem_mode = 'timing'               # Use timing accesses
  system.mem_ranges = [AddrRange('512MB')] # Create an address range

  # Create a simple CPU
  system.cpu = TimingSimpleCPU()

  # Create an L1 instruction and data cache
  system.cpu.icache = L1ICache()
  system.cpu.dcache = L1DCache()

  # Connect the instruction and data caches to the CPU
  system.cpu.icache_port = system.cpu.icache.cpu_side
  system.cpu.dcache_port = system.cpu.dcache.cpu_side

  # Create a memory bus, a coherent crossbar, in this case
  system.l2bus = L2XBar()

  # Hook the CPU ports up to the l2bus
  system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
  system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

  # Create an L2 cache and connect it to the l2bus
  system.l2cache = L2Cache()
  system.l2bus.mem_side_ports = system.l2cache.cpu_side

  # Create a memory bus, a system crossbar, in this case
  system.membus = SystemXBar()

  # Connect the L2 cache to the membus
  system.l2cache.mem_side = system.membus.cpu_side_ports

  # create the interrupt controller for the CPU and connect to the membus
  system.cpu.createInterruptController()

  # Create a DDR3 memory controller and connect it to the membus
  system.mem_ctrl = MemCtrl()
  system.mem_ctrl.dram = DDR3_1600_8x8()
  system.mem_ctrl.dram.range = system.mem_ranges[0]
  system.mem_ctrl.port = system.membus.mem_side_ports

  # Connect the system up to the membus
  system.system_port = system.membus.cpu_side_ports

  # Create a process for a simple "Hello World" application
  process = Process()
  # Set the command
  # cmd is a list which begins with the executable (like argv)
  process.cmd = [sys.argv[2]]
  # Set the cpu to use the process as its workload and create thread contexts
  system.cpu.workload = process
  system.cpu.createThreads()

  # set up the root SimObject and start the simulation
  root = Root(full_system = False, system = system)

  return system


def runSystem(system):
  # instantiate all of the objects we've created above
  m5.instantiate()

  print("Beginning simulation!")
  exit_event = m5.simulate()
  print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
