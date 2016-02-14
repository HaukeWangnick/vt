''' 
:mod:`argutils`
===============

This module provides additional argument types for use with the standard `argparse` module.
'''

import os
import argparse

def _checkexisting(path,exist,fmt=None,join=None):
    ''' Checks whether `path` (appended with `join` if not :const:`None`) `exist` (or not). 
    Returns path, or else raises :exc:`ArgumentTypeError` (with `fmt`\ %\ `path` as error text, 
    using a default text if :const:`None`). Internal function for use by :func:`existingtype`.
    '''
    orig = path
    if join: path = os.path.join(path,join)
    if os.path.exists(path)!=exist:
        if fmt is None: fmt = '%s doesn\'t exist' if exist else '%s already exists'
        raise argparse.ArgumentTypeError(fmt%path)
    return orig
             
def existingtype(exist,fmt=None,join=None):
    ''' Returns a function that takes a path as single argument which then calls :func:`_checkexisting`
    with `exist`, `fmt` and `join` as additional arguments.
    The function returned is meant to be used as `type` for command line argument parsing via `argparse`.
    '''
    return lambda path: _checkexisting(path,exist,fmt,join)
