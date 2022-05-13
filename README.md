# JPath2022

This code relates to the paper "Deep Learning-Based Histotype Diagnosis of Ovarian Carcinoma Whole-Slide Pathology Images" (the link, citation, and a figure from the paper will be added when it is published)

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


# Models

We compared the performance of four deep learning architectures. Here are links to the implementations of each model.

1. One-stage Transfer Learning (1STL)
2. DeepMIL
3. VarMIL 
4. Two-Stage Transfer Learning (2STL) https://github.com/AIMLab-UBC/MIDL2020