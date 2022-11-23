"""seperation of labels

Seperates the small and the bigger structure from the test files and puts it to new folder
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


def process(id_: str, paths: dict, labels: list):
    """Loads and processes an image.

    The processing includes:

    - Delete labels not specified in labels

    Args:
        id_ (str): An image identifier.
        paths (dict): A dict, where the keys are an image identifier of type structure.BrainImageTypes
            and the values are paths to the images.
        labels (list): A list, where the labels are defined which should be kept.
    """

    print('-' * 10, 'Processing', id_)

    # load image
    # path = paths.pop(id_, '')  # the value with key id_ is the root directory of the image
    path_to_process = paths.pop(structure.BrainImageTypes.GroundTruth.name, '')
    ground_truth = sitk.ReadImage(path_to_process)

    ground_truth_array = sitk.GetArrayFromImage(ground_truth)
    # np.where(ground_truth_array is labels, [ground_truth_array, 0])
    mask = np.isin(ground_truth_array, labels)
    ground_truth_masked = ground_truth_array * mask

    ground_truth_labeled = sitk.GetImageFromArray(ground_truth_masked)
    ground_truth_labeled.CopyInformation(ground_truth)

    sitk.WriteImage(ground_truth_labeled, path_to_process)


def process_batch(data_batch: t.Dict[structure.BrainImageTypes, structure.BrainImage],
                  labels: dict = None) -> t.List[structure.BrainImage]:
    """Loads and processes a batch of images.

    The processing includes:

    - Keep specified labels

    Args:
        data_batch (Dict[structure.BrainImageTypes, structure.BrainImage]): Batch of images to be processed.
        labels (list): Labels to keep.
    """
    labels_list = list(labels.keys())
    params_list = list(data_batch.items())
    [process(id_, path, labels_list) for id_, path in params_list]


@hydra.main(version_base=None, config_path="conf", config_name="config")
def label_separation(cfg: DictConfig):
    """Brain label separation.

        The label seperation:

            - copies the train and test data if needed
            - searches for the ground truth of the data
            - in big structures the labels for the smalls are deleted
            - in small structures the labels for the big are deleted
            - Input labels will be deleted
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
    # for directory in os.listdir(cfg.pipeline.paths.data_train_dir):
    #     img_dir = os.path.join(cfg.pipeline.paths.data_train_dir, directory)
    #
    #     if os.path.exists(os.path.join(img_dir, 'labels_native.nii.gz')):
    #         ground_truth = sitk.ReadImage(os.path.join(img_dir, 'labels_native.nii.gz'))
    #
    #         ground_truth_array = sitk.GetArrayFromImage(ground_truth)
    #         np.where(ground_truth_array not in cfg.pipeline.params.labels, [0, ground_truth_array])
    #
    #         ground_truth_labeled = sitk.GetImageFromArray(ground_truth_array)
    #         ground_truth_labeled.CopyInformation(ground_truth)
    #
    #         sitk.WriteImage(ground_truth_labeled, os.path.join(img_dir, 'labels_native.nii.gz'))


if __name__ == "__main__":
    """The program's entry point."""

    # script_dir = os.path.dirname(sys.argv[0])
    #
    # parser = argparse.ArgumentParser(description='Medical label separation for brain tissue segmentation')
    #
    # parser.add_argument(
    #     '--new_train_dir',
    #     type=str,
    #     default=os.path.normpath(os.path.join(script_dir, '../data/train_big/')),
    #     help='Directory for separated train labels.'
    # )
    #
    # parser.add_argument(
    #     '--new_test_dir',
    #     type=str,
    #     default=os.path.normpath(os.path.join(script_dir, '../data/test_big/')),
    #     help='Directory for separated train labels.'
    # )
    #
    # parser.add_argument(
    #     '--data_train_dir',
    #     type=str,
    #     default=os.path.normpath(os.path.join(script_dir, '../data/train/')),
    #     help='Directory with training data.'
    # )
    #
    # parser.add_argument(
    #     '--data_test_dir',
    #     type=str,
    #     default=os.path.normpath(os.path.join(script_dir, '../data/test/')),
    #     help='Directory with test data.'
    # )
    #
    # parser.add_argument(
    #     '--labels',
    #     type=list,
    #     default=[1, 2],
    #     help='Labels to preserve.'
    # )
    #
    # args = parser.parse_args()
    # label_separation(args.new_train_dir, args.new_test_dir, args.data_train_dir, args.data_test_dir)
    label_separation()
