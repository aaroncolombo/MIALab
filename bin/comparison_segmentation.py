"""comparison of metrics

Compare the metrics of the pipeline calculating all labels to the pipeline calculating the separated labels
"""
import shutil
import os
import sys
import glob

import SimpleITK as sitk
import numpy as np
import typing as t
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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


def plot(result_file: str, result_dir: str):
    """
    plot the Dice coefficients per label (i.e. white matter, gray matter, hippocampus, amygdala, thalamus)
    in a boxplot
    """

    sns.boxplot(x='LABEL', y='DICE', hue='pipeline', data=result_file)
    plt.ylim(0, 1)
    plt.title("Dice value combined pipeline compared to original pipeline")
    plt.savefig(os.path.join(result_dir, 'boxplot_dice.png'), format="png")
    plt.show()

    sns.boxplot(x='LABEL', y='HDRFDST', hue='pipeline', data=result_file)
    plt.ylim(0, 40)
    plt.title("Hausdorff value combined pipeline compared to original pipeline")
    plt.savefig(os.path.join(result_dir, 'boxplot_hdrfst.png'), format="png")
    plt.show()

    return 0


@hydra.main(version_base=None, config_path="conf", config_name="config")
def combine(cfg: DictConfig):
    """
    TODO: Write docstring
    """

    # Define the paths
    if not os.path.isdir(cfg.paths.gen_result_dir):
        raise ValueError('root_dir {} does not exist'.format(cfg.paths.gen_result_dir))

    # search the root directory for result the last created day directory
    day_result_dir = max(glob.glob(os.path.join(cfg.paths.gen_result_dir, '*')), key=os.path.getmtime)

    # search the result day directory for last created time directory
    time_result_dir = max(glob.glob(os.path.join(day_result_dir, '*')), key=os.path.getmtime)

    # ignore hydra directories
    result_dirs = glob.glob(os.path.join(time_result_dir, 'mia-result_*'))

    # define empty data frame to combine the interim results
    df_comb = pd.DataFrame(data={'SUBJECT': [], 'LABEL': [], 'DICE': [], 'HDRFDST': []})
    for result_dir in result_dirs:
        if 'mia-result_all' in result_dir:
            df_all = pd.DataFrame(pd.read_csv(os.path.join(result_dir, 'results.csv'), sep=";"))
        if 'mia-result_all' not in result_dir:
            df_inter = pd.DataFrame(pd.read_csv(os.path.join(result_dir, 'results.csv'), sep=";"))
            df_comb = pd.merge_ordered(df_comb, df_inter, how='outer')

    # result dir for the combined data and the plots.
    comb_result_dir = os.path.join(time_result_dir, 'mia-result_combine/')  # to be defined
    os.makedirs(comb_result_dir, exist_ok=True)

    # save the combined results and make a column from which pipeline the results are
    df_comb.columns = ['SUBJECT', 'LABEL', 'DICE', 'HDRFDST']
    df_comb['pipeline'] = 'combined pipeline'
    df_all['pipeline'] = 'original pipeline'
    df_comb.to_csv(comb_result_dir + 'results_combined.csv', index=True)

    # add the assembled results of the different pipelines to the original pipeline to compare the data
    df_comp = pd.concat([df_all, df_comb], axis=0, join='outer')
    # save as csv
    df_comp.to_csv(comb_result_dir + 'results_compare.csv', index=True)

    plot(df_comp, comb_result_dir)

    # dir_all = os.path.join(result_dir_path, 'mia-result_all/results.csv')  # to be defined
    # if not os.path.isfile(dir_all):
    #     raise ValueError('root_dir {} does not exist'.format(dir_all))
    # dir_big = os.path.join(result_dir_path, 'mia-result_big/results.csv')  # to be defined
    # if not os.path.isfile(dir_big):
    #     raise ValueError('root_dir {} does not exist'.format(dir_big))
    # dir_small = os.path.join(result_dir_path, 'mia-result_small/results.csv')  # to be defined
    # if not os.path.isfile(dir_small):
    #     raise ValueError('root_dir {} does not exist'.format(dir_small))
    #
    # end_dir = os.path.join(time_result_dir, 'mia-result_combine/')  # to be defined
    # os.makedirs(end_dir, exist_ok=True)
    #
    # dfA = pd.DataFrame(pd.read_csv(dir_all, sep=";"))
    # dfB = pd.DataFrame(pd.read_csv(dir_big, sep=";"))
    # dfS = pd.DataFrame(pd.read_csv(dir_small, sep=";"))
    #
    # data_merged_right = pd.merge_ordered(dfB, dfS, how='outer')
    # bs_column_names = ['SUBJECT BS', 'LABEL BS', 'DICE BS', 'HDRFDST BS']
    # data_merged_right.columns = bs_column_names
    #
    # data_merged_right.to_csv(end_dir + 'Big_Small_Merged.csv', index=True)
    #
    # df_merged = pd.concat([dfA, data_merged_right], axis=1)
    # df_merged_smaller = df_merged.drop(axis=1, columns=['SUBJECT BS', 'LABEL BS'])
    #
    # df_merged_smaller.to_csv(end_dir + 'all_right.csv', index=True)


# for testing
if __name__ == '__main__':
    combine()
