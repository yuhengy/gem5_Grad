
#include <map>

#include "mem/cache/rekey_miss_addr_cache.hh"

#include "base/types.hh"
#include "mem/cache/tags/base_set_assoc.hh"
#include "params/RekeyMissAddrCache.hh"

#define MAX_ENTRY_IN_EVICTHISTORY 1000

RekeyMissAddrCache::RekeyMissAddrCache(const RekeyMissAddrCacheParams *p)
    : Cache(p),
      maxEvictPerEpoch(p->max_evict_per_epoch)
{}

void
RekeyMissAddrCache::evictBlock(CacheBlk *blk, PacketList &writebacks)
{

    // STEP1 log access history
    static std::map<Addr, uint32_t> evictHistory;
    static uint32_t maxNumEvict = 0;
    // STEP2 get addr
    Addr blkAddr = tags->regenerateBlkAddr(blk);
    auto iter = evictHistory.find(blkAddr);
    // STEP3 increment the history
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
    // STEP4 for debug
    stats.replacementsDefineEpoch++;

    // STEP5 flush if necessary
    // NOTE: maxEvictPerEpoch==2 means 
    //       the second time you want to evict one addr,
    //       flush will be triggered
    // NOTE: maxEvictPerEpoch is at least 2
    if (maxNumEvict == maxEvictPerEpoch) {
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

RekeyMissAddrCache*
RekeyMissAddrCacheParams::create()
{
    assert(tags);
    assert(replacement_policy);

    return new RekeyMissAddrCache(this);
}
