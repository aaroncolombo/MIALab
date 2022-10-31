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

def label_separation(new_train_dir: str, new_test_dir: str, data_train_dir: str, data_test_dir: str):
    """Brain label separation.

        The main routine executes the medical image analysis pipeline:

            - Image loading
            - Registration
            - Pre-processing
            - Feature extraction
            - Decision forest classifier model building
            - Segmentation using the decision forest classifier model on unseen images
            - Post-processing of the segmentation
            - Evaluation of the segmentation
    """
    #  TODO: change the wording of the docstring

    #  TODO: if the new directories do not exist create them
    #  TODO: copy the data directories in the new directories

    #  TODO: Get the different ground truth maps of each patient
    # crawler = futil.FileSystemDataCrawler(data_train_dir,
    #                                       LOADING_KEYS,
    #                                       futil.BrainImageFilePathGenerator(),
    #                                       futil.DataDirectoryFilter())

    #  TODO: Delete the obsolete labels in each label map


if __name__ == "__main__":
    """The program's entry point."""

    script_dir = os.path.dirname(sys.argv[0])

    parser = argparse.ArgumentParser(description='Medical label separation for brain tissue segmentation')

    parser.add_argument(
        '--new_train_dir',
        type=str,
        default=os.path.normpath(os.path.join(script_dir, './data/train_big/')),
        help='Directory for separated train labels.'
    )

    parser.add_argument(
        '--new_test_dir',
        type=str,
        default=os.path.normpath(os.path.join(script_dir, './data/test_big/')),
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
        help='Directory with testing data.'
    )

    args = parser.parse_args()
    label_separation(args.new_train_dir, args.new_test_dir, args.data_train_dir, args.data_test_dir)