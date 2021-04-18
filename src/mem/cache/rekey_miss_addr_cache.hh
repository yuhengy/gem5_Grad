
#ifndef __MEM_CACHE_REKEY_MISS_ADDR_CACHE_HH__
#define __MEM_CACHE_REKEY_MISS_ADDR_CACHE_HH__

#include "mem/cache/cache.hh"

struct RekeyMissAddrCacheParams;

class RekeyMissAddrCache : public Cache
{
  protected:
    const uint64_t maxEvictPerEpoch;

  protected:
    void evictBlock(CacheBlk *blk, PacketList &writebacks);

  public:
    RekeyMissAddrCache(const RekeyMissAddrCacheParams *p);
};

#endif // __MEM_CACHE_REKEY_MISS_ADDR_CACHE_HH__
