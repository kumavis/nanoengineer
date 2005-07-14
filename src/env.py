# Copyright (c) 2005 Nanorex, Inc.  All rights reserved.
'''
env.py

A place for global variables treated as "part of the environment".

$Id$

This module is for various global or "dynamic" variables,
which can be considered to be part of the environment of the code
that asks for them (thus the module name "env"). This is for variables
which are used by lots of code, but which would be inconvenient to pass
as arguments (since many routines would need to pass these through
without using them), and which some code might want to change dynamically
to provide a modified environment for some of the code it calls.

(Many of these variables will need to be thread-specific if we ever have threads.)

Also, certain basic routines for using/allocating some of these global variables.


Usage:

import env

   ... use env.xxx as needed ...
   # Don't say "from env import xxx" since env.xxx might be reassigned dynamically.
   # Variables that never change (and are importable when the program is starting up)
   # can be put into constants.py


Purpose and future plans:

Soon we should move some more variables here from platform, assy, win, and/or globalParms,
especially win.history (as a place to record things, of which there is one at a time,
even if we someday have more than one widget to view it, and change it dynamically to record
object-specific histories -- well, in that case an object-attr might be appropriate,
but not an assy or win attr like now!).

We might also put some "dynamic variables" here, like the current Part --
this is not yet decided.

Generators used to allocate things also might belong here, whether or not
we have global dicts of allocated things. (E.g. the one for atom keys.)

The main test of whether something might belong here is whether there will always be at most one
of them per process (or per active thread), even when we support multiple open files,
multiple main windows, multiple glpanes and model trees, etc.


History:

bruce 050610 made this module (since we've needed it for awhile), under the name "globals.py"
(since "global" is a Python keyword).

bruce 050627 renamed this module to "env.py", since "globals" is a Python builtin function.
'''

__author__ = 'bruce'

from constants import *
import platform

_last_glselect_name = 0

obj_with_glselect_name = {} # public for lookup ###e this needs to be made weak-valued ASAP! #######@@@@@@@

def new_glselect_name():
    "Return a session-unique 32-bit unsigned int for use as a GL_SELECT name."
    #e We could recycle these for dead objects (and revise docstring),
    # but that's a pain, and unneeded (I think), since it's very unlikely
    # we'll create more than 4 billion objects in one session.
    global _last_glselect_name
    _last_glselect_name += 1
    return _last_glselect_name

def alloc_my_glselect_name(obj):
    "Register obj as the owner of a new GL_SELECT name, and return that name."
    name = new_glselect_name()
    obj_with_glselect_name[name] = obj
    return name

# dict for atoms or singets whose element type, atomtype, or set of bonds (or neighbors) gets changed [bruce 050627]

_changed_structure_atoms = {} # maps id(atom) to atom, for atoms or singlets

# the beginnings of a general change-handling scheme [bruce 050627]

def post_event_updates( warn_if_needed = False ): #####@@@@@ call this from lots of places, not just update_parts like now
    """[public function]
       This should be called at the end of every user event which might have changed
    anything in any loaded model which defers some updates to this function.
    (Someday there will be a general way for models to register their updaters here,
    so that they are called in the proper order. For now, that's hardcoded.)
       This can also be called at the beginning of user events, such as redraws or saves,
    which want to protect themselves from event-processors which should have called this
    at the end, but forgot to. Those callers should pass warn_if_needed = True, to cause
    a debug-only warning to be emitted if the call was necessary. (This function is designed
    to be very fast when called more times than necessary.)
    """
    if not _changed_structure_atoms: #e this will be generalized to: if no changes of any kind, since the last call
        return
    # some changes occurred, so this function needed to be called (even if they turn out to be trivial)
    if warn_if_needed and platform.atom_debug:
        # whichever user event handler made these changes forgot to call this function when it was done!
        print "atom_debug: post_event_updates should have been called before, but wasn't!" #e use print_compact_stack??
        pass # (other than printing this, we handle unreported changes normally)
    # handle and clear all changes since the last call
    # (in the proper order, when there might be more than one kind of change #nim)
    if _changed_structure_atoms:
        import bond_updater
        ##Comented out by Huaicai 7/14/05, a potential problem if reload from a zip file.
        #reload(bond_updater) # during devel, reload this module every time it's used
        from bond_updater import update_bonds_after_each_event
        update_bonds_after_each_event( _changed_structure_atoms)
            #e not sure if that routine will need to use or change other similar globals in this module;
            # if it does, passing just that one might be a bit silly (so we could pass none, or all affected ones)
        _changed_structure_atoms.clear()
    return

# end