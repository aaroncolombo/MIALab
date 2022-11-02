"""seperation of labels

Seperates the small and the bigger structure from the test files and puts it to new folder
"""
import os
import sys
import shutil



# src_file = os.path.join((os.path.dirname(sys.argv[0])), '../data/test/')
# shutil.copy2(src_file,src_file)




#script_dir = os.path.dirname(sys.argv[0])

#parser = argparse.ArgumentParser(description='Medical image analysis pipeline for brain tissue segmentation')

#parser.add_argument(
#        '--data_test_dir',
#        type=str,
#        default=os.path.normpath(os.path.join(script_dir, '../data/test/')),
#        help='Directory with testing data.'
#    )

#args = parser.parse_args()


#args.data_test_dir

import argparse
import os
import sys
import timeit
import warnings

import SimpleITK as sitk
import numpy as np
import pymia.data.conversion as conversion
import pymia.evaluation.writer as writer

try:
    import mialab.data.structure as structure
    import mialab.utilities.file_access_utilities as futil
except ImportError:
    # Append the MIALab root directory to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '..'))
    import mialab.data.structure as structure
    import mialab.utilities.file_access_utilities as futil

LOADING_KEYS = [structure.BrainImageTypes.GroundTruth]  # the list of data we will load

#def label_separation(new_train_dir: str, new_test_dir: str, data_train_dir: str, data_test_dir: str, labels: list):
def label_separation(new_train_dir: str, new_test_dir: str, data_train_dir: str, data_test_dir: str):
    """Brain label separation.

        The label seperation:

            - copies the train and test data if needed
            - searches for the ground truth of the data
            - in big structures the labels for the smalls are deleted
            - in small structures the labels for the big are deleted
            - Input labels will be delelted
    """
    # labels for big and small seperation
    labels = [1, 2]

    # check if train folder exists
    if not os.path.exists(new_train_dir):
        os.makedirs(new_train_dir)

    # check if test folder exists
    if not os.path.exists(new_test_dir):
        os.makedirs(new_test_dir)

    # copy the data into the new directories
    shutil.copytree(data_train_dir, new_train_dir, dirs_exist_ok=True)
    shutil.copytree(data_test_dir, new_test_dir, dirs_exist_ok=True)

    #  TODO: Get the different ground truth maps of each patient
    crawler = futil.FileSystemDataCrawler(data_train_dir,
                                          LOADING_KEYS,
                                          futil.BrainImageFilePathGenerator(),
                                          futil.DataDirectoryFilter())




    #  TODO: Delete the obsolete labels in each label map
    for directory in os.listdir(new_train_dir):
        img_dir = os.path.join(new_train_dir, directory)

        if os.path.exists(os.path.join(img_dir,'labels_native.nii.gz')):
            ground_truth = sitk.ReadImage(os.path.join(img_dir,'labels_native.nii.gz'))

            ground_truth_array = sitk.GetArrayFromImage(ground_truth)
            for label in labels:
                ground_truth_array[ground_truth_array == label] = 0

            ground_truth_labeled = sitk.GetImageFromArray(ground_truth_array)
            ground_truth_labeled.CopyInformation(ground_truth)

            sitk.WriteImage(ground_truth_labeled, os.path.join(img_dir,'labels_native.nii.gz'))


if __name__ == "__main__":
    """The program's entry point."""

    script_dir = os.path.dirname(sys.argv[0])

    parser = argparse.ArgumentParser(description='Medical label separation for brain tissue segmentation')

    parser.add_argument(
        '--new_train_dir',
        type=str,
        default=os.path.normpath(os.path.join(script_dir, '../data/train_big/')),
        help='Directory for separated train labels.'
    )

    parser.add_argument(
        '--new_test_dir',
        type=str,
        default=os.path.normpath(os.path.join(script_dir, '../data/test_big/')),
        help='Directory for separated train labels.'
    )

    parser.add_argument(
        '--data_train_dir',
        type=str,
        default=os.path.normpath(os.path.join(script_dir, '../data/train/')),
        help='Directory with training data.'
    )

    parser.add_argument(
        '--data_test_dir',
        type=str,
        default=os.path.normpath(os.path.join(script_dir, '../data/test/')),
        help='Directory with test data.'
    )

    parser.add_argument(
        '--labels',
        type=list,
        default=[1, 2],
        help='Labels to preserve.'
    )

    args = parser.parse_args()
    label_separation(args.new_train_dir, args.new_test_dir, args.data_train_dir, args.data_test_dir)
