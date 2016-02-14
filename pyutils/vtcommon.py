'''
:mod:`vtcommon.py
=================

This module provides functionality of the Virtualisation Toolkit common to multiple scripts.
'''

import os
import sys
import shutil

import call

def projectinit(name,vtdir,template,gitinit=True):
    try:
        shutil.copytree(os.path.join(vtdir,'resources',template),name,symlinks=True)
    except OSError as exc:
        sys.exit('%s when initialising project directory from template'%exc)

    if gitinit:
        try:
            os.chdir(name)
            call.call('git init',5)
        except call.callError as exc:
            sys.exit('Project directory created, but git init failed (%s)'%exc)
