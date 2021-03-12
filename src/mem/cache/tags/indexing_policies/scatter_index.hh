
#ifndef __MEM_CACHE_INDEXING_POLICIES_SCATTER_INTEX_HH__
#define __MEM_CACHE_INDEXING_POLICIES_SCATTER_INTEX_HH__

#include "mem/cache/tags/indexing_policies/skewed_associative.hh"
#include "params/ScatterIndex.hh"

class ScatterIndex : public SkewedAssociative
{
  private:


  public:
    /**
     * Construct and initialize this policy.
     */
    ScatterIndex(const ScatterIndexParams *p);

    /**
     * Destructor.
     */
    ~ScatterIndex() {};
};

#endif //__MEM_CACHE_INDEXING_POLICIES_SCATTER_INTEX_HH__
