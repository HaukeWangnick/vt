''' 
:mod:`argutils`
===============

This module provides additional argument types for use with the standard `argparse` module.
'''

import os
import argparse

def _checkexisting(path,exist,fmt=None,join=None):
    ''' Checks whether `path` (appended with `join` if not :const:`None`) `exist` (or not).
    
    Args:
        path (str): Path to check for (non-) existance.
        exist (bool): Whether `path` should exist or not.
        fmt (str): Error message to use in case of failure. Must contain %s to show the path.
        join (str): Additional path component to append to `path`.
        
    Returns:
        (str): Given `path`.
        
    Raises:
        ArgumentTypeError: When path existance is not as expected. 
    
    Internal function for use by :func:`existingtype`.
    '''
    orig = path
    if join: path = os.path.join(path,join)
    if os.path.exists(path)!=exist:
        if fmt is None: fmt = '%s doesn\'t exist' if exist else '%s already exists'
        raise argparse.ArgumentTypeError(fmt%path)
    return orig
             
def existingtype(exist,fmt=None,join=None):
    ''' Creates a function that takes a path as single argument, 
    which then calls :func:`_checkexisting` together with the parameters provided.
    
    Args:
        exist, fmt, join: Refer to :func:`_checkexisting`.
        
    Returns:
        Function usable as `type` for command line argument parsing via `argparse`.
    '''
    return lambda path: _checkexisting(path,exist,fmt,join)
