
#ifndef __MEM_CACHE_REKEY_CACHE_HH__
#define __MEM_CACHE_REKEY_CACHE_HH__

#include "mem/cache/cache.hh"

struct RekeyCacheParams;

class RekeyCache : public Cache
{
  protected:
    const uint64_t maxEvictPerEpoch;

  protected:
    void evictBlock(CacheBlk *blk, PacketList &writebacks);

  public:
    RekeyCache(const RekeyCacheParams *p);
};

#endif // __MEM_CACHE_REKEY_CACHE_HH__
