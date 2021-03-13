
from m5.objects import SkewedAssociative

from baseConfig import configSystem, runSystem


system = configSystem(useRekeyCache=True)
system.l2cache.tags.indexing_policy = SkewedAssociative()
runSystem(system)
