'''
:mod:`vtcommon`
===============

This module provides functionality of the Virtualisation Toolkit common to multiple scripts.
'''

import os
import sys
import shutil

import call

def projectinit(name,template,git=True):
    ''' Create a VT project directory by copying from a template resource tree.
    
    `name` is the name of the new VT project directory.
    `template` is the template directory to copy from.
    `git` specifies whether to prepare the project directory for Git use.
    
    Attention: :func:`os.chdir`\ s into the new VT project directory!
    
    Calls :func:`sys.exit` upon errors.
    '''
    try:
        shutil.copytree(template,name,symlinks=True)
    except OSError as exc:
        sys.exit('%s when initialising project directory from template'%exc)

    if git:
        try:
            os.chdir(name)
            call.call('git init',5)
            call.call('git add .',5)
        except call.callError as exc:
            sys.exit('Project directory created, but git initialization failed (%s)'%exc)
