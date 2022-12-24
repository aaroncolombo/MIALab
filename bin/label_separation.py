"""Separation of labels

Separates the structure from the test files and puts it to new folder
"""
import shutil
import os
import sys

import SimpleITK as sitk
import numpy as np
import typing as t

import hydra
from omegaconf import DictConfig

try:
    import mialab.data.structure as structure
    import mialab.utilities.file_access_utilities as futil
except ImportError:
    # Append the MIALab root directory to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))
    import mialab.data.structure as structure
    import mialab.utilities.file_access_utilities as futil


def process(id_: str, paths: dict, labels: list) -> None:
    """Loads and processes one image.

    The processing includes:
        - Delete labels not specified in labels

    Params:
        id_ (str): An image identifier.
        paths (dict): A dict, where the keys are an image identifier of type structure.BrainImageTypes
            and the values are paths to the images.
        labels (list): A list, where the labels are defined which should be kept.

    Returns:
        None
    """

    print('-' * 10, 'Processing', id_)

    # Load image
    # path = paths.pop(id_, '')  # the value with key id_ is the root directory of the image
    path_to_process = paths.pop(structure.BrainImageTypes.GroundTruth.name, '')
    ground_truth = sitk.ReadImage(path_to_process)

    # Convert image to numpy array
    ground_truth_array = sitk.GetArrayFromImage(ground_truth)
    # Build mask for the labels to keep
    mask = np.isin(ground_truth_array, labels)
    # Delete the unwanted labels by multiplication with zero
    ground_truth_masked = ground_truth_array * mask
    # Convert numpy array to simple itk image
    ground_truth_labeled = sitk.GetImageFromArray(ground_truth_masked)
    ground_truth_labeled.CopyInformation(ground_truth)
    # Save the image
    sitk.WriteImage(ground_truth_labeled, path_to_process)


def process_batch(data_batch: t.Dict[structure.BrainImageTypes, structure.BrainImage],
                  labels: dict = None) -> t.List[structure.BrainImage]:
    """Loads and processes a batch of images.

    The processing includes:
        - Process one image of the batch

    Params:
        data_batch (Dict[structure.BrainImageTypes, structure.BrainImage]): Batch of images to be processed.
        labels (list): Labels to keep.

    Returns:
        None
    """
    labels_list = list(labels.keys())
    params_list = list(data_batch.items())
    [process(id_, path, labels_list) for id_, path in params_list]


@hydra.main(version_base=None, config_path="conf", config_name="config")
def label_separation(cfg: DictConfig) -> None:
    """Brain label separation.

    The label separation:
        - copies the train and test data if needed
        - searches for the ground truth of the data
        - Deletes the unwanted labels from the ground truth

    Params:
        cfg (DictConfig): Hydra configuration file

    Returns:
        None
    """

    # check if train folder exists
    if not os.path.exists(cfg.pipeline.paths.data_train_dir):
        os.makedirs(cfg.pipeline.paths.data_train_dir, exist_ok=True)
    # check if test folder exists
    if not os.path.exists(cfg.pipeline.paths.data_test_dir):
        os.makedirs(cfg.pipeline.paths.data_test_dir, exist_ok=True)

    # copy the data into the new directories
    shutil.copytree(cfg.paths.data_train_dir_orig,
                    cfg.pipeline.paths.data_train_dir,
                    dirs_exist_ok=True)
    shutil.copytree(cfg.paths.data_test_dir_orig,
                    cfg.pipeline.paths.data_test_dir,
                    dirs_exist_ok=True)

    # crawl the training image directories
    crawler_train = futil.FileSystemDataCrawler(cfg.pipeline.paths.data_train_dir,
                                                cfg.pipeline.params.loading_keys_labels,
                                                futil.BrainImageFilePathGenerator(),
                                                futil.DataDirectoryFilter())
    # crawl the testing image directories
    crawler_test = futil.FileSystemDataCrawler(cfg.pipeline.paths.data_test_dir,
                                               cfg.pipeline.params.loading_keys_labels,
                                               futil.BrainImageFilePathGenerator(),
                                               futil.DataDirectoryFilter())

    for crawler in [crawler_train, crawler_test]:
        process_batch(crawler.data, cfg.pipeline.params.labels)


if __name__ == "__main__":
    """The program's entry point."""
    label_separation()
