
#include <map>

#include "mem/cache/rekey_miss_cache.hh"

#include "base/types.hh"
#include "mem/cache/tags/base_set_assoc.hh"
#include "params/RekeyMissCache.hh"

#define MAX_ENTRY_IN_EVICTHISTORY 1000

RekeyMissCache::RekeyMissCache(const RekeyMissCacheParams *p)
    : Cache(p),
      maxEvictPerEpoch(p->max_evict_per_epoch)
{}

void
RekeyMissCache::evictBlock(CacheBlk *blk, PacketList &writebacks)
{

    // STEP1 log access history
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

    else {
        PacketPtr pkt = Cache::evictBlock(blk);
        if (pkt) {
            writebacks.push_back(pkt);
        }
    }

}

RekeyMissCache*
RekeyMissCacheParams::create()
{
    assert(tags);
    assert(replacement_policy);

    return new RekeyMissCache(this);
}
