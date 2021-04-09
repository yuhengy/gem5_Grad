
#include <map>

#include "mem/cache/rekey_hit_cache.hh"

#include "base/types.hh"
#include "mem/cache/tags/base_set_assoc.hh"
#include "params/RekeyHitCache.hh"


RekeyHitCache::RekeyHitCache(const RekeyHitCacheParams *p)
    : Cache(p),
      maxEvictPerEpoch(p->max_evict_per_epoch)
{}


// NOTE: all name of evict actually should be access.
//       For easy implementing, I do not change them.
bool
RekeyHitCache::access(PacketPtr pkt, CacheBlk *&blk, Cycles &lat,
                      PacketList &writebacks)
{
    // STEP1 log num Acc
    static uint64_t numEvict = 0;
    numEvict++;

    // STEP2 for debug
    stats.replacementsDefineEpoch++;

    // STEP3 flush if necessary
    // NOTE: maxEvictPerEpoch==2 means 
    //       the second time you want to evict one addr,
    //       flush will be triggered
    // NOTE: maxEvictPerEpoch is at least 2
    if (numEvict == maxEvictPerEpoch) {
        for (CacheBlk& blk_anyone :
            static_cast<BaseSetAssoc*>(tags)->getBlks()) {
            if (blk_anyone.isValid()) {
                stats.numFlushInvalid++;
                PacketPtr pkt = Cache::evictBlock(&blk_anyone);
                if (pkt) {
                    if (pkt->cmd == MemCmd::WritebackDirty ||
                        pkt->cmd == MemCmd::WriteClean) {
                        stats.numFlushWB++;
                    }
                    writebacks.push_back(pkt);
                }
            }
        }
        stats.numEpoch++;
        numEvict = 0;
    }

    // STEP4 do normal access
    return Cache::access(pkt, blk, lat, writebacks);
}


RekeyHitCache*
RekeyHitCacheParams::create()
{
    assert(tags);
    assert(replacement_policy);

    return new RekeyHitCache(this);
}
