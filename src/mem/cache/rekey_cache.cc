
#include "mem/cache/rekey_cache.hh"

#include "params/RekeyCache.hh"

RekeyCache::RekeyCache(const RekeyCacheParams *p)
    : Cache(p)
{}

RekeyCache*
RekeyCacheParams::create()
{
    assert(tags);
    assert(replacement_policy);

    return new RekeyCache(this);
}
