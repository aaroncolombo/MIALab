"""Comparison of classifiers

Compare the metrics of the original pipeline to the separated pipeline.
"""
import os
import sys
import glob

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


def plot(result_file: pd.DataFrame, result_dir: str) -> None:
    """Plot a boxplot

    Plots a boxplot to compare the pipelines per metric and label.

    Params:
        result_file (pd.DataFrame): Data frame containing the results of the original and combined pipelines.
        result_dir (str): Path to the directory.

    Returns:
        None
    """
    # Plot boxplot for the DICE
    sns.boxplot(x='LABEL', y='DICE', hue='pipeline', data=result_file)
    plt.ylim(0, 1)
    plt.title("Dice value combined pipeline compared to original pipeline")
    plt.savefig(os.path.join(result_dir, 'boxplot_dice.png'), format="png")
    plt.show()

    # Plot boxplot for the Hausdorff distance
    sns.boxplot(x='LABEL', y='HDRFDST', hue='pipeline', data=result_file)
    plt.ylim(0, 40)
    plt.title("Hausdorff value combined pipeline compared to original pipeline")
    plt.savefig(os.path.join(result_dir, 'boxplot_hdrfst.png'), format="png")
    plt.show()


@hydra.main(version_base=None, config_path="conf", config_name="config")
def combine(cfg: DictConfig) -> None:
    """Combines the result files of the original and separated pipelines.

    The combine routine contains the following steps:
        - Search for the latest created results folder
        - Creating a data frame for all results
        - Load the result data frame from the original pipeline
        - Load and combine all result files from the separated pipelines
        - Creating a data frame to compare the combined results with the original results
        - Plot the results

    Params:
        cfg (DictConfig): Hydra configuration file containing all necessary paths.

    Returns:
        None
    """

    # Define the paths
    if not os.path.isdir(cfg.paths.gen_result_dir):
        raise ValueError('root_dir {} does not exist'.format(cfg.paths.gen_result_dir))

    # Search the root directory for result the last created day directory
    day_result_dir = max(glob.glob(os.path.join(cfg.paths.gen_result_dir, '*')), key=os.path.getmtime)

    # Search the result day directory for last created time directory
    time_result_dir = max(glob.glob(os.path.join(day_result_dir, '*')), key=os.path.getmtime)

    # Ignore hydra directories
    result_dirs = glob.glob(os.path.join(time_result_dir, 'mia-result_*'))

    # Define empty data frame to combine the interim results
    df_comb = pd.DataFrame(data={'SUBJECT': [], 'LABEL': [], 'DICE': [], 'HDRFDST': []})
    for result_dir in result_dirs:
        if 'mia-result_all' in result_dir:
            df_all = pd.DataFrame(pd.read_csv(os.path.join(result_dir, 'results.csv'), sep=";"))
        if 'mia-result_all' not in result_dir:
            df_inter = pd.DataFrame(pd.read_csv(os.path.join(result_dir, 'results.csv'), sep=";"))
            df_comb = pd.merge_ordered(df_comb, df_inter, how='outer')

    # Result dir for the combined data and the plots.
    comb_result_dir = os.path.join(time_result_dir, 'mia-result_combine/')  # to be defined
    os.makedirs(comb_result_dir, exist_ok=True)

    # Save the combined results and make a column from which pipeline the results are
    df_comb.columns = ['SUBJECT', 'LABEL', 'DICE', 'HDRFDST']
    df_comb['pipeline'] = 'combined pipeline'
    df_all['pipeline'] = 'original pipeline'
    df_comb.to_csv(comb_result_dir + 'results_combined.csv', index=True)

    # Add the assembled results of the different pipelines to the original pipeline to compare the data
    df_comp = pd.concat([df_all, df_comb], axis=0, join='outer')
    # Save as csv and plot the results
    df_comp.to_csv(comb_result_dir + 'results_compare.csv', index=True)
    plot(df_comp, comb_result_dir)


# for testing
if __name__ == '__main__':
    """The program's entry point."""
    combine()
