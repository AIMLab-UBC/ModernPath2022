# ModernPath2022

![alt text](https://github.com/AIMLab-UBC/ModernPath2022/blob/main/docs/Figure_1.tif)

This code relates to the paper "Deep Learning-Based Histotype Diagnosis of Ovarian Carcinoma Whole-Slide Pathology Images" (the link and citation will be added when it is published)

This repository covers two main features implemented in the paper: 1. the color normalization strategy used and 2. the implementations of the deep convolutional neural networks that were compared

# Color Normalization

The color normalization strategy used in this paper was first introduced in "[The utility of color normalization for AI-based diagnosis of hematoxylin and eosin-stained pathology images](https://onlinelibrary.wiley.com/doi/abs/10.1002/path.5797)"

```
@article{boschman2022utility,
  title={The utility of color normalization for AI-based diagnosis of hematoxylin and eosin-stained pathology images},
  author={Boschman, Jeffrey and Farahani, Hossein and Darbandsari, Amirali and Ahmadvand, Pouya and Van Spankeren, Ashley and Farnell, David and Levine, Adrian B and Naso, Julia R and Churg, Andrew and Jones, Steven JM and others},
  journal={The Journal of Pathology},
  volume={256},
  number={1},
  pages={15--24},
  year={2022},
  publisher={Wiley Online Library}
}
```
### Installation

1. Install required packages

The suggested strategy is to create a conda environment with Python 3.8, install the [staintools](https://staintools.readthedocs.io/en/latest/) package using pip, and install all the other packages using conda.

```
conda create -n cn_env python=3.8
conda activate cn_env
conda install -c conda-forge python-spams=2.6.1
pip install staintools==2.1.2
conda install psutil=5.8.0
conda install tqdm=4.64.0
```

2. Clone this repo
```
mkdir color_normalization
cd color_normalization
git clone https://github.com/AIMLab-UBC/ModernPath2022
cd ModernPath2022
```

### Running color normalization
Here is an example command that creates normalized copies of image patches, where each patch is randomly normalized using 1 of 2 color normalization methods (reinhard and vahadane) and 1 of 3 reference images (ref1.png, ref2.png, ref3.png).
```
python3 app_color_norm.py --methods reinhard vahadane --patch_location <path/to/ModernPath2022>/sample_images/orig_patches --norm_location <path/to/ModernPath2022>/sample_images/norm_patches --reference_images <path/to/ModernPath2022>/sample_images/ref1.png <path/to/ModernPath2022>/sample_images/ref2.png <path/to/ModernPath2022>/sample_images/ref3.png --patch_pattern ''
```

# Models

We compared the performance of four deep learning architectures. Here are links to the implementations of each model.

1. One-stage Transfer Learning (1STL)
2. [DeepMIL](https://github.com/AIMLab-UBC/EC2022) (This repository is private, and will be made public following the publication of a different paper)
3. [VarMIL](https://github.com/AIMLab-UBC/EC2022) (This repository is private, and will be made public following the publication of a different paper)
4. [Two-Stage Transfer Learning (2STL)](https://github.com/AIMLab-UBC/MIDL2020)
