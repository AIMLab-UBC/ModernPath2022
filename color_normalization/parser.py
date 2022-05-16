import argparse
from utils.utilities import dir_path, file_path

def create_parser():
    parser = argparse.ArgumentParser(description=''' Perform color normalization ''')

    parser.add_argument('--methods', nargs="+", type=str, required=False, default='vahadane',
        help="""The Normalization method(s). Options are vahadane, macenko, or reinhard.
        Multiple reference images can be used - just separate them with a space""")

    parser.add_argument('--patch_location', type=dir_path, required=True,
        help="""The full path to the head folder where the patches are located, before taking into account the patch_pattern.""")

    parser.add_argument('--norm_location', type=dir_path, required=True,
        help="""The full path to the head folder where the normalized patches will be saved. The directory stucture will be the same as for patch_location (i.e., will use the patch_pattern directory structure.)""")

    parser.add_argument('--reference_image',  nargs="+", type=file_path, required=True,
        help="""The path to reference image(s) for normalization.
        Multiple reference images can be used - just separate them with a space.""")

    parser.add_argument("--num_patch_workers", type=int,
        help="""Number of worker processes to multi-process patch extraction.
        Default sets the number of worker processes to the number of CPU processes.""")

    parser.add_argument("--patch_pattern", type=str,
        default='annotation/subtype/slide',
        help="""'/' separated words describing the directory structure of the patch_location. For example, if the patch files are saved according to the directory structure: /path/to/patch/rootdir/Tumor/P53ABN/case_1234/40x/patch1.png, and the patch_location is /path/to/patch/rootdir/Tumor, then the patch_pattern might be subtype/slide/magnification.""")

    parser.add_argument('--use_standardizer', action='store_true',
        help="""Whether to apply brighness standarizer on the images.
        Note: This could cause huge changes on your result, so need to be checked.
        The official website mentioned that it can improve the tissue mask calculation""")

    parser.add_argument('--use_multiple_CPUs', action='store_true',
        help="""If this flag is set, instead of loading num_patch_workers slides in
        each run, only one slide is loaded. It is usefull when slides have a lot of patches.""")

    parser.add_argument("--seed", type=int,
                        default=1234,
                        help="Seed for random library.")

    return parser
