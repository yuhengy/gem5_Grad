
#include "mem/cache/rekey_cache.hh"

#include "mem/cache/tags/base_set_assoc.hh"
#include "params/RekeyCache.hh"

RekeyCache::RekeyCache(const RekeyCacheParams *p)
    : Cache(p),
      maxEvictPerEpoch(p->max_evict_per_epoch)
{}

void
RekeyCache::evictBlock(CacheBlk *blk, PacketList &writebacks)
{

    static uint64_t numEvict = 0;

    if (numEvict == maxEvictPerEpoch) {
        for (CacheBlk& blk_anyone :
            static_cast<BaseSetAssoc*>(tags)->getBlks()) {
            if (blk_anyone.isValid()) {
                PacketPtr pkt = Cache::evictBlock(&blk_anyone);
                if (pkt) {
                    writebacks.push_back(pkt);
                }
            }
        }
        stats.numEpoch++;
        numEvict = 0;
    }
    else {
        PacketPtr pkt = Cache::evictBlock(blk);
        if (pkt) {
            writebacks.push_back(pkt);
        }
    }

    numEvict++;
    stats.replacementsDefineEpoch++;
}

RekeyCache*
RekeyCacheParams::create()
{
    assert(tags);
    assert(replacement_policy);

    return new RekeyCache(this);
}
