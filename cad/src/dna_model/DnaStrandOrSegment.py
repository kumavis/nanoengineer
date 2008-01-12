# Copyright 2007 Nanorex, Inc.  See LICENSE file for details. 
"""
DnaStrandOrSegment.py - ... 

@author: Bruce
@version: $Id$
@copyright: 2007 Nanorex, Inc.  See LICENSE file for details.
"""

from Group import Group
from dna_model.DnaGroup import DnaGroup

class DnaStrandOrSegment(Group):
    #e maybe inherit some more special subclass of Group? May not matter since we ourselves never show up in MT.
    """
    Abstract superclass for DnaStrand and DnaSegment,
    which represent a Dna Strand or Dna Segment inside a Dna Group.

    Internally, this is just a specialized Group containing various
    subobjects:

    - as Group members (not visible in MT, but for convenience of
    reusing preexisting copy/undo/mmp code):

      - one or more DnaAtomMarkers, one of which determines this
        strand's or segment's base indexing, and whether/how it survives if its
        chains of PAM atoms are broken or merged with other strands or segments

      - (maybe) this DnaStrands's DnaStrandChunks, or this DnaSegment's
        DnaAxisChunks (see docstrings of DnaStrand/DnaSegment for details)

    - As other attributes:

      - (probably) a chain of DnaAtomChainOrRings
        which together comprise all the PAM atoms in this strand, or all
        the PAM atoms in the axis of this segment. From these,
        related objects like DnaLadders and connected DnaSegments/DnaStrands
        can be found. (But we may instead have, or also have and mainly use,
        a chain of the chunks that normally contain these same atoms.
        The reason we might need both is that the atom-based chain,
        independent of chunks, can help the dna updater reconstruct
        the chunks after a change by old code which didn't do that itself.
    
      - whatever other properties the user needs to assign, which are not
        covered by the member nodes or superclass attributes. However,
        some of these might be stored on the controlling DnaAtomMarker,
        so that if we are merged with another strand or segment, and later separated
        again, that marker can again control the properties of a new strand
        or segment (as it
        will in any case control its base indexing).
    """

    def get_DnaGroup(self):
        """
        Return the DnaGroup we are contained in, or None if we're not
        inside one.
        
        @note: Returning None should never happen
        if we have survived a run of the dna updater.
        """
        return self.parent_node_of_class( DnaGroup)

    pass

# end
