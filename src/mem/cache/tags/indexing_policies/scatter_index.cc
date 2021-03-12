
#include "mem/cache/tags/indexing_policies/scatter_index.hh"

#include "mem/cache/tags/indexing_policies/QARMA64.c"

ScatterIndex::ScatterIndex(const ScatterIndexParams *p)
    : SkewedAssociative(p)
{}

ScatterIndex *
ScatterIndexParams::create()
{
    return new ScatterIndex(this);
}
