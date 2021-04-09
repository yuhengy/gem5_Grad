
#ifndef __MEM_CACHE_REKEY_MISS_CACHE_HH__
#define __MEM_CACHE_REKEY_MISS_CACHE_HH__

#include "mem/cache/cache.hh"

struct RekeyMissCacheParams;

class RekeyMissCache : public Cache
{
  protected:
    const uint64_t maxEvictPerEpoch;

  protected:
    void evictBlock(CacheBlk *blk, PacketList &writebacks);

  public:
    RekeyMissCache(const RekeyMissCacheParams *p);
};

#endif // __MEM_CACHE_REKEY_MISS_CACHE_HH__
