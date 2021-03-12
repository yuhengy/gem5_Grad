
from m5.objects import ScatterIndex

from baseConfig import configSystem, runSystem


system = configSystem()
system.l2cache.tags.indexing_policy = ScatterIndex()
runSystem(system)
