import os.path
import glob
import panda as pd


def combine():
    script_dir = os.path.dirname(__file__)
    dir_all = os.path.join(script_dir, './mia-result/2022-10-10-21-12-42/results.csv') #to be defined
    dir_big = os.path.join(script_dir, './mia-result/2022-10-10-21-12-42/results.csv') #to be defined
    dir_small = os.path.join(script_dir, './mia-result/2022-10-10-21-12-42/results.csv') #to be defined
    end_dir = os.path.join(script_dir, './mia-results/')

    data =[]
    dataA = pd.read_csv(dir_all, sep=";")
    dataB = pd.read_csv(dir_big, sep=";")
    dataS = pd.read_csv(dir_small, sep=";")

    data.append(dataA)
    data.append(dataB)
    data.append(dataS)

    data_merged = pd.concat(data, ignore_index=True)

    data_merged.to_csv(end_dir+ 'results_comnbined.csv', index = False)