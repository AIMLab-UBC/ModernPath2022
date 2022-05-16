import os
os.environ['KMP_WARNINGS'] = 'off' #if you want to see the OMP warning, comment out this line
import numpy as np
import staintools
import psutil
import warnings
import random
from tqdm import tqdm
from PIL import Image
import multiprocessing as mp
import utils.utilities as utils

class ColorNormalization(object):
    """Normalize patches"

    Attributes
    ----------
    methods : str
        Normalization method(s)

    patch_location : str
        Path to root directory containing all of the patches

    norm_location : str
        Path to root directory storing all of the normalized patches

    reference_images : str
        Path(s) to reference image(s) for normalization.

    no_luminosity_standardization : bool
        Whether to use force no luminosity standardization on images. Default is to use luminosity standardization unless an error occurs, in which case standardization is turned off.

    patch_pattern : Dict
        Dictionary describing the directory structure of the patch paths.
        A non-multiscale patch can be contained in a directory /path/to/patch/rootdir/Tumor/MMRD/VOA-1234/1_2.png so its patch_pattern is annotation/subtype/slide.
        A multiscale patch can be contained in a directory /path/to/patch/rootdir/Stroma/P53ABN/VOA-1234/10/3_400.png so its patch pattern is annotation/subtype/slide/magnification

#J    num_patch_workers : int

    """

    def __init__(self, config):
        self.methods = config.methods
        self.patch_location = config.patch_location
        self.norm_location = config.norm_location
        self.reference_images = config.reference_images
        self.use_standardizer = config.use_standardizer
        self.use_multiple_CPUs = config.use_multiple_CPUs
        self.n_process = psutil.cpu_count() if self.use_multiple_CPUs else 1
        self.patch_pattern = utils.create_patch_pattern(config.patch_pattern)
        self.patch_paths = utils.get_patch_paths(self.patch_location, self.patch_pattern)

    def normalize_patches(self, normalizer, patch_path, norm_path):
        """Normalize patches and store them

        Parameters
        ----------
        normalizer : transformer
            Normalize patches

        patch_path : str
            Path of patch that is going to be normalized

        norm_path :str
            Path of normalized patch
        """
        try:
            patch = np.array(Image.open(patch_path))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                if self.use_standardizer:
                    patch = staintools.LuminosityStandardizer.standardize(patch)
                norm  = normalizer(patch.copy())
            norm  = Image.fromarray(norm)
            norm.save(norm_path)
        except:
            print(f" The patch with path {patch_path} is blank!!")

    def stain_normalizers(self):
        """
        Calculate a list of normalizers
        """
        normalizers = []
        for method in self.methods:
            for reference_image in self.reference_images:
                if method == 'reinhard':
                    normalizer = staintools.ReinhardColorNormalizer()
                else:
                    normalizer = staintools.StainNormalizer(method=method)

                target = np.array(Image.open(reference_image))
                if self.use_standardizer:
                    target = staintools.LuminosityStandardizer.standardize(target)
                normalizer.fit(target)
                normalizers.append(normalizer.transform)
        print(f"Each patch will be normalized randomly by one of {len(normalizers)} normalizers")
        return normalizers

    def produce_args(self, normalizers, cur_patch_paths):
        """Produce arguments to send to patch extraction subprocess. Creates subdirectories for patches if necessary.

        Parameters
        ----------
        normalizers : array of staintools
            transformer

        cur_patch_paths : list of str
            List of patch paths.

        Returns
        -------
        list of tuple
            List of argument tuples to pass through each process. Each argument tuple contains:
             - normalizer (transformer) used to normalize patches
             - patch_path (str) path of patch that is going to be normalized
             - norm_path (str) path of normalized patch
        """
        args = []
        for patch_path in cur_patch_paths:
            norm_path  = patch_path.replace(self.patch_location,
                                            self.norm_location)
            dirname = utils.get_dirname_of(norm_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            # If the file does not exist
            # Suitable for when we add some data to existing directory
            if not os.path.isfile(norm_path):
                arg = (random.choice(normalizers), patch_path, norm_path)
                args.append(arg)
        return args

    def run(self):
        """
        Run color normalization
        """
        print(f"Number of CPU processes: {self.n_process}")
        mp.set_start_method('spawn')
        n_patches = len(self.patch_paths)
        prefix = f'Normalizing {n_patches} patches: '
        try:
            normalizers = self.stain_normalizers()
        except:
            self.use_standardizer = False
            print("Luminosity standardizer set to False")
            normalizers = self.stain_normalizers()
        with mp.Pool(processes=self.n_process) as pool:
            for idx in tqdm(range(0, n_patches, self.n_process),
                    desc=prefix, dynamic_ncols=True):
                cur_patch_paths = self.patch_paths[idx:idx + self.n_process]
                tasks = []
                for args in self.produce_args(normalizers, cur_patch_paths):
                    tasks.append(list(args))
                pool.starmap(self.normalize_patches, tasks)
            pool.close()
            pool.join()
        print("Done.")
