
#include <map>

#include "mem/cache/rekey_cache.hh"

#include "base/types.hh"
#include "mem/cache/tags/base_set_assoc.hh"
#include "params/RekeyCache.hh"

#define MAX_ENTRY_IN_EVICTHISTORY 1000

RekeyCache::RekeyCache(const RekeyCacheParams *p)
    : Cache(p),
      maxEvictPerEpoch(p->max_evict_per_epoch)
{}

void
RekeyCache::evictBlock(CacheBlk *blk, PacketList &writebacks)
{

    //static uint64_t numEvict = 0;
    //numEvict++;
    // STEP1 log access history
    static std::map<Addr, uint32_t> evictHistory;
    static uint32_t maxNumEvict = 0;
    // STEP1.1 get addr
    Addr blkAddr = tags->regenerateBlkAddr(blk);
    auto iter = evictHistory.find(blkAddr);
    // STEP1.2 increment the history
    if (iter == evictHistory.end()) {
        evictHistory[blkAddr] = 1;
    }
    else {
        (iter->second)++;
        if ((iter->second) > maxNumEvict) {
            maxNumEvict = (iter->second);
        }
    }
    // STEP1.3 shrink the history if too large
    if (evictHistory.size() == MAX_ENTRY_IN_EVICTHISTORY) {
        for (auto iter = evictHistory.begin();
                  iter != evictHistory.end(); iter++) {
            if ((iter->second) < (maxNumEvict/10 + 1)) {
                evictHistory.erase(iter);
            }
        }
    }
    // STEP1.4 for debug
    stats.replacementsDefineEpoch++;

    // STEP2 flush if necessary
    // NOTE: maxEvictPerEpoch==2 means 
    //       the second time you want to evict one addr,
    //       flush will be triggered
    // NOTE: maxEvictPerEpoch is at least 2
    //if (numEvict == maxEvictPerEpoch) {
    if (maxNumEvict == maxEvictPerEpoch) {
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
        //numEvict = 0;
        evictHistory.clear();
        maxNumEvict = 0;
    }

    else {
        PacketPtr pkt = Cache::evictBlock(blk);
        if (pkt) {
            writebacks.push_back(pkt);
        }
    }

}

RekeyCache*
RekeyCacheParams::create()
{
    assert(tags);
    assert(replacement_policy);

    return new RekeyCache(this);
}
