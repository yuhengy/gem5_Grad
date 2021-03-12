
from m5.objects import SkewedAssociative

from baseConfig import configSystem, runSystem


system = configSystem()
system.l2cache.tags.indexing_policy = SkewedAssociative()
runSystem(system)
