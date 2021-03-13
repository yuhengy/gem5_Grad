
#ifndef __MEM_CACHE_REKEY_CACHE_HH__
#define __MEM_CACHE_REKEY_CACHE_HH__

#include "mem/cache/cache.hh"

struct RekeyCacheParams;

/**
 * A coherent cache that can be arranged in flexible topologies.
 */
class RekeyCache : public Cache
{
  protected:

  public:
    /** Instantiates a basic cache object. */
    RekeyCache(const RekeyCacheParams *p);
};

#endif // __MEM_CACHE_REKEY_CACHE_HH__
