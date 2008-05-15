# Copyright 2006-2008 Nanorex, Inc.  See LICENSE file for details. 
"""
GlobalPreferences.py

Routines that test for various global user preferences.

Note: this module is likely to be imported early, and should be
considered a low level support module.  As such, importing it should
not drag in much else.  As of 2007/09/05, that's probably not true
yet. [That goal may be impractical and not really necessary, given
the kinds of things in it so far -- bruce 080220 comment]

@author: Eric Messick
@version: $Id$
@copyright: 2006-2008 Nanorex, Inc.  See LICENSE file for details.
"""

from utilities.prefs_constants import permit_atom_chunk_coselection_prefs_key
from utilities.debug_prefs import debug_pref, Choice_boolean_False, Choice_boolean_True
from utilities.debug import print_compact_traceback

# ==

DEBUG_BAREMOTION = False #bruce 080129, for bug 2606; should be disabled for commits

DEBUG_BAREMOTION_VERBOSE = False

# ==

_pyrex_atoms_failed = False
_pyrex_atoms_succeeded = False
_pyrex_atoms_unwanted_this_session = False

def usePyrexAtomsAndBonds(): #bruce 080218, revised/renamed 080220
    """
    Should we, and if so can we successfully, import the necessary symbols
    from atombase (compiled from atombase.pyx and associated files)
    for using the "Pyrex atoms" C/Pyrex code to optimize classes Atom and Bond?
    """
    global _pyrex_atoms_failed, _pyrex_atoms_succeeded, _pyrex_atoms_unwanted_this_session

    if _pyrex_atoms_failed or _pyrex_atoms_unwanted_this_session:
        return False
    if _pyrex_atoms_succeeded:
        return True

    res = debug_pref("Enable pyrex atoms in next session?",
                     Choice_boolean_False,
                     ## non_debug = True, # revised this option and menu text (thus prefs key), bruce 080221
                         # make this ATOM_DEBUG only for release (since it's a slowdown), bruce 080408
                     prefs_key = True)

    # uncomment the following line to temporarily override the above debug_pref,
    # e.g. to recover from trying it out and having it abort NE1 on startup
    # (hypothetical error, not known to happen):

    ## res = False # do not commit with this line active

    if res:
        # make sure it works, before telling caller to use it
        try:
            _test_atombase()
        except:
            # note: the known possible exceptions would be caught by
            # "except (ImportError, ValueError):"
            _pyrex_atoms_failed = True # don't try it again
            msg = "exception importing atombase as requested -- won't use it: "
            print_compact_traceback(msg)
            import foundation.env as env # import cycle??
            # note: in present implem of history [080220], this is printed too
            # early to show up in the widget, but hopefully that will be fixed
            env.history.redmsg("ERROR: unable to use experimental Pyrex Atoms and Bonds from atombase module; see console prints")
            res = False
        else:
            _pyrex_atoms_succeeded = True
            # for now, we need a can't miss note for success, as well (red, though not an error):
            print "\nNOTE: using experimental Pyrex Atoms and Bonds from atombase module\n"
            import foundation.env as env # import cycle??
            env.history.redmsg("NOTE: using experimental Pyrex Atoms and Bonds from atombase module")
        pass

    if not res:
        _pyrex_atoms_unwanted_this_session = True # might be because it failed

    assert _pyrex_atoms_failed or _pyrex_atoms_succeeded or _pyrex_atoms_unwanted_this_session
        # be sure we make up our mind whether to use them only once per session
        # (so debug pref change does not take effect until we rerun NE1)

    return res

def _test_atombase():
    import atombase # this must not be made into a toplevel import!
    from atombase import AtomBase, AtomDictBase, BondBase, BondDictBase
    return

def debug_pyrex_atoms():
    res = debug_pref("debug pyrex atoms?",
                     Choice_boolean_False,
                     ## non_debug = True,
                         # make ATOM_DEBUG only for release (not useful enough
                         # for non_debug), bruce 080408
                     prefs_key = True )
    return res
# ==

# bruce 060721; was intended to become constant True for A9; as of 080320 it's not planned for A10
# but might be good to try to get to afterwards

def permit_atom_chunk_coselection():
    res = debug_pref("permit atom/chunk coselection?",
                     ## use Choice_boolean_True once this has no obvious bugs
                     Choice_boolean_False,
                     ## non_debug = True,
                         # make ATOM_DEBUG only for release (since maybe unsafe,
                         # not useful since unsupported), bruce 080408
                     prefs_key = permit_atom_chunk_coselection_prefs_key )
    return res

# ==

def disable_do_not_draw_open_bonds():
    """
    Whether to disable all behavior which under some conditions
    refrains from drawing open bonds or bondpoints
    which would be drawn according to "traditional" rules
    (those in place before 2007).

    Can be useful for debugging, if the developer remembers it's enabled.
    """
    res = debug_pref("DNA: draw all open bonds?",
                         # the name starts with DNA because the special rules
                         # it turns off only affect DNA
                     Choice_boolean_False,
                     non_debug = True, #bruce 080406
                         # leave this visible w/o ATOM_DEBUG for release [bruce 080408]
                     prefs_key = True)
    return res

# ==

def _debug_pref_use_dna_updater(): #bruce 080320 moved this here from master_model_updater.py, made private
    res = debug_pref("DNA: enable dna updater?", #bruce 080317 revised text
                     Choice_boolean_True, #bruce 080317 False -> True
                     ## non_debug = True,
                         # make ATOM_DEBUG only for release (since unsafe to change (undo bugs),
                         # not useful since off is more and more unsupported), bruce 080408
                     prefs_key = "A10/DNA: enable dna updater?" #bruce 080317 changed prefs_key
                 )
    return res

def dna_updater_is_enabled(): #bruce 080320
    return _debug_pref_use_dna_updater()

# ==

def debug_pref_enable_pam_convert_sticky_ends(): #bruce 080514; remove when this feature works
    res = debug_pref("DNA: enable PAM3+5 for sticky ends? [nim]",
                     Choice_boolean_False,
                     prefs_key = True)
    return res

# ==

def debug_pref_write_bonds_compactly(): #bruce 080328
    # note: reading code for this was made active in same commit, 080328.
    # note: this could be used for non-dna single bond chains too,
    #  so the function name, preks_key, and associated abstract methods
    #  needn't contain the term "dna", though the menu text is clearer
    #  by containing it.
    res = debug_pref("mmp format: write dna bonds compactly?",
                     Choice_boolean_False,
                     # we will change this to True as soon as all developers
                     # have the necessary reading code
                     non_debug = True,
                     prefs_key = "A10/mmp format: write bonds compactly? "
                 )
    return res

def debug_pref_read_bonds_compactly(): #bruce 080328
    res = debug_pref("mmp format: read dna bonds compactly?",
                     Choice_boolean_True, # use False to simulate old reading code for testing
                     ## non_debug = True, # temporary
                         # make ATOM_DEBUG only for release (not useful enough
                         # for non_debug), bruce 080408
                     prefs_key = True # temporary
                 )
    return res

# exercise them, to put them in the menu
debug_pref_write_bonds_compactly()
debug_pref_read_bonds_compactly()

# ==

def debug_pref_write_new_display_names(): #bruce 080328
    # note: reading code for this was made active a few days before 080328;
    # this affects *all* mmp files we write (for save, ND1, NV1)
    res = debug_pref("mmp format: write new display names?",
                     # we will change this to True as soon as all developers
                     # have the necessary reading code... doing that, 080410
                     Choice_boolean_True,
                     non_debug = True,
                     prefs_key = "A10/mmp format: write new display names?"
                 )
    return res

def debug_pref_read_new_display_names(): #bruce 080328
    res = debug_pref("mmp format: read new display names?",
                     Choice_boolean_True, # use False to simulate old reading code for testing
                     ## non_debug = True, # temporary
                         # make ATOM_DEBUG only for release (not useful enough
                         # for non_debug), bruce 080408
                     prefs_key = True # temporary
                 )
    return res

# exercise them, to put them in the menu
debug_pref_write_new_display_names()
debug_pref_read_new_display_names()

# ==

def use_frustum_culling(): #piotr 080401
    """
    If enabled, perform frustum culling in GLPane.
    """
    res = debug_pref("GLPane: enable frustum culling?",
                     Choice_boolean_True,
                     non_debug = True,
                         # leave this visible w/o ATOM_DEBUG for release
                         # [bruce 080408]
                     prefs_key = "A10/GLPane: enable frustum culling?") 

    return res

# ==

def pref_indicate_overlapping_atoms(): #bruce 080411
    res = debug_pref("GLPane: indicate overlapping atoms?",
                     Choice_boolean_False,
                         # not on by default, since experimental, and in case
                         # initial implem is slow (it has to scan all atoms of
                         #  all chunks, though it doesn't disable their display
                         #  lists for their regular drawing). We might revise
                         # this (after the pcoming release) if it's safe and
                         # can be made to be fast.
                     non_debug = True, # since potentially very useful for users
                     prefs_key = "A10/GLPane: indicate overlapping atoms? " )
    return res

# ==

def pref_MMKit_include_experimental_PAM_atoms(): #bruce 080412
    res = debug_pref("MMKit: include experimental PAM atoms (next session)?",
                     Choice_boolean_False,
                         # not on by default, and not visible without ATOM_DEBUG,
                         # since these elements would confuse users
                     prefs_key = "A10/MMKit: include experimental PAM atoms?" )
    return res

# ==

def pref_drop_onto_Group_puts_nodes_at_top(): #bruce 080414; added after 1.0.0rc0 was made
    """
    If enabled, nodes dropped directly onto Groups in the Model Tree
    are placed at the beginning of their list of children,
    not at the end as was done before.
    """
    res = debug_pref("Model Tree: drop onto Group puts nodes at top?",
                     Choice_boolean_True, # this default setting fixes a longstanding NFR
                     non_debug = True,
                         # leave this visible w/o ATOM_DEBUG for release
                         # [bruce 080414]
                     prefs_key = "A10/Model Tree: drop onto Group puts nodes at top?")

    return res

pref_drop_onto_Group_puts_nodes_at_top()
    # exercise it at startup to make sure it's in the debug prefs menu
    # TODO: have an init function in this file, run after history is available ###
    # (not sure if first import of this file is after that)

# ==

def _kluge_global_mt_update():
    from foundation import env
        # note: this doesn't cause a module import cycle,
        # but it might be an undesirable inter-package import.
        # (it's also done in a few other places in this file.)
    win = env.mainwindow()
    win.mt.mt_update()
    return
    
def pref_show_node_color_in_MT():
    #bruce 080507, mainly for testing new MT method repaint_some_nodes;
    # won't yet work for internal groups that act like MT leaf nodes
    # such as DnaStrand
    """
    If enabled, show node colors in the Model Tree.
    """
    res = debug_pref("Model Tree: show node colors?",
                     Choice_boolean_False,
                     prefs_key = True,
                     call_with_new_value = (lambda val: _kluge_global_mt_update())
                    )
    return res
    
def pref_show_highlighting_in_MT():
    #bruce 080507
    """
    If enabled, highlighting objects in GLPane causes corresponding
    highlighting in the MT of their containing nodes,
    and (in future) mouseovers in MT may also cause highlighting
    in both places.
    """
    res = debug_pref("Model Tree: show highlighted objects?",
                     Choice_boolean_True,
                     non_debug = True,
                     prefs_key = True,
                     call_with_new_value = (lambda val: _kluge_global_mt_update())
                    )
    return res

# ==

def pref_minimize_leave_out_PAM_bondpoints():
    #bruce 080507
    """
    If enabled, bondpoints on PAM atoms are left out of simulations
    and minimizations, rather than being converted to H (as always occurred
    until now) or anchored or left unchanged (not yet possible).

    @warning: not yet fully implemented.
    """
    res = debug_pref("Minimize: leave out PAM bondpoints? (partly nim)",
                     Choice_boolean_False, # not yet safe or tested (and partly nim)
                     non_debug = True, # should be easy to test
                     prefs_key = True
                    )
    return res

pref_minimize_leave_out_PAM_bondpoints()

# end
