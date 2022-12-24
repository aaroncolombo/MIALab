"""Plot the results of the grid search

The grid search optimizes two parameters of a decision forest classifier
"""
import os
import argparse

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def main(result_file: str) -> None:
    """Plot the metrics of the grid search for brain tissue classifier.

    Params:
        result_file (str): The path to the results file.

    Returns:
        None
    """
    # Load result file as data frame
    df = pd.read_csv(result_file, sep=";")
    # Get the directory from the result file path
    result_dir = os.path.dirname(result_file)
    # Get a list of unique values in the label column
    labels = df["LABEL"].unique()
    for x, label in enumerate(labels):
        # Create a data frame for each label
        df_label = df.loc[df["LABEL"] == label]
        for y1, metric in enumerate(df_label["METRIC"].unique()):
            # Create a data frame for each metric
            df_label_metric = df_label.loc[df_label["METRIC"] == metric]
            for y2, statistic in enumerate(df_label_metric["STATISTIC"].unique()):
                # Create a data frame for each statistic (mean or std)
                df_label_metric_statistic_long = df_label_metric.loc[df_label_metric["STATISTIC"] == statistic]
                # Convert the data frame to a pivot table for the grid plot
                df_label_metric_statistic = df_label_metric_statistic_long.pivot("N_ESTIMATOR", "MAX_DEPTH", "VALUE")
                # Define the bounds of the plot
                if metric == "DICE":
                    if statistic == "MEAN":
                        v_min, v_max = 0, 1
                    else:
                        v_min = df_label_metric_statistic_long["VALUE"].min()
                        df_max = df_label_metric_statistic_long.loc[df_label_metric_statistic_long["VALUE"] != np.inf]
                        v_max = df_max["VALUE"].max()
                else:
                    if statistic == "MEAN":
                        v_min = df_label_metric_statistic_long["VALUE"].min()
                        df_max = df_label_metric_statistic_long.loc[df_label_metric_statistic_long["VALUE"] != np.inf]
                        v_max = df_max["VALUE"].max()
                    else:
                        v_min = df_label_metric_statistic_long["VALUE"].min()
                        df_max = df_label_metric_statistic_long.loc[df_label_metric_statistic_long["VALUE"] != np.inf]
                        v_max = df_max["VALUE"].max()
                # Draw a heatmap with the numeric values in each cell
                sns.heatmap(df_label_metric_statistic, cmap="crest", vmin=v_min, vmax=v_max,
                            annot=True, fmt=".3f", linewidths=.5).set(title=" ".join([label, metric, statistic]), )
                # Generate specific name and save the plot
                name = "_".join([label, metric, statistic])
                plt.savefig(result_dir + "/" + name + ".pdf", format='pdf')
                plt.show()

# for testing
if __name__ == '__main__':
    """The programs entry point"""
    parser = argparse.ArgumentParser(description='Plot the results of a grid search.')

    parser.add_argument(
        '--result_file',
        type=str,
        default=os.path.normpath("/Users/aaroncolombo/Library/CloudStorage/OneDrive-UniversitaetBern/MIALab/results/gridsearch/ResultAll/all_overview_plot.csv"),
        help='File containing the results.'
    )
    args = parser.parse_args()

    main(args.result_file)
