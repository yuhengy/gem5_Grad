
#ifndef __MEM_CACHE_REKEY_HIT_CACHE_HH__
#define __MEM_CACHE_REKEY_HIT_CACHE_HH__

#include "mem/cache/cache.hh"

struct RekeyHitCacheParams;

class RekeyHitCache : public Cache
{
  protected:
    const uint64_t maxEvictPerEpoch;

  protected:
    bool access(PacketPtr pkt, CacheBlk *&blk, Cycles &lat,
                PacketList &writebacks) override;

  public:
    RekeyHitCache(const RekeyHitCacheParams *p);
};

#endif // __MEM_CACHE_REKEY_HIT_CACHE_HH__
