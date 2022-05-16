import os
import glob
import argparse

def set_random_seed(seed_value):
    # 1. Set `PYTHONHASHSEED` environment variable at a fixed value
    try:
        import os
        os.environ['PYTHONHASHSEED'] = str(seed_value)
    except:
        pass
    # 2. Set `python` built-in pseudo-random generator at a fixed value
    try:
        import random
        random.seed(seed_value)
    except:
        pass
    # 3. Set `numpy` pseudo-random generator at a fixed value
    try:
        import numpy as np
        np.random.seed(seed_value)
    except:
        pass

    # 4. Set `pytorch` pseudo-random generator at a fixed value
    try:
        import torch
        torch.manual_seed(seed_value)
    except:
        pass
    print(f"random_seed set to={seed_value}")

def create_patch_pattern(patch_pattern):
    '''Given a string of '/' separated words, create a dict of the words and their ordering in the string.

    Parameters
    ----------
    patch_pattern : str
        String of '/' separated words

    Returns
    -------
    dict
        Empty dict if patch pattern is '', otherwise each word becomes a dict key with int ID giving position of the key in patch pattern.
    '''
    if patch_pattern == '' or patch_pattern == "'":
        return {}
    else:
        if type(patch_pattern) is str:
            patch_pattern = patch_pattern.split('/')
        return {k: i for i, k in enumerate(patch_pattern)}

def get_patch_paths(rootpath, pattern, extensions = ['png']):
    '''Function to get a list of all the patches to be normalized'''
    """Get paths for files including paths for slides and patches.

    Parameters
    ----------
    rootpath : str
        The rootpath

    pattern : dict
        The slide or patch pattern. If pattern is passed, then we only retrieve file paths that have the same path length (i.e. item_path.split('/') are all the same length)

    extensions : list of str
        List of file extensions to search for

    Returns
    -------
    list of str
        List of slide paths
    """
    paths = []
    for extension in extensions:
        path_wildcard = rootpath
        if pattern is None:
            path_wildcard = os.path.join(path_wildcard, '**', '*.' + extension)
            paths.extend(glob.glob(path_wildcard, recursive=True))
        else:
            for i in range(len(pattern)):
                path_wildcard = os.path.join(path_wildcard, '**')
            path_wildcard = os.path.join(path_wildcard, '*.' + extension)
            paths.extend(glob.glob(path_wildcard))
    return paths

def get_dirname_of(filepath):
    """Get absolute path of the immediate directory the file is in

    Parameters
    ----------
    filepath : str
        The path i.e. /path/to/TCGA-A5-A0GH-01Z-00-DX1.22005F4A-0E77-4FCB-B57A-9944866263AE.svs

    Returns
    -------
    str
        The dirname i.e /path/to
    """
    return os.path.dirname(os.path.abspath(filepath))


def dir_path(s):
    if os.path.isdir(s):
        return s
    else:
        try:
            os.makedirs(s, exist_ok=True)
            return s
        except:
            raise argparse.ArgumentTypeError(f"readable_dir:{s} is not a valid path")


def file_path(s):
    if os.path.isfile(s):
        return s
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{s} is not a valid path")
