import os.path
import glob
import pandas as pd


def combine():
    script_dir = os.path.dirname(__file__)
    # test path
    #script_dir = 'C:/Users/zahir/Documents/Studies/MSc_Bern/3_Semester/MIALab/bin/'
    dir_all = os.path.join(script_dir, './mia-result/2022-10-10-21-12-42/results.csv')  # to be defined
    dir_big = os.path.join(script_dir, './mia-result/2022-10-17-16-14-02_Big/results.csv')  # to be defined
    dir_small = os.path.join(script_dir, './mia-result/2022-10-17-16-14-02_Small/results.csv')  # to be defined
    end_dir = os.path.join(script_dir, './combine_results/')  # to be defined
    if not os.path.exists(end_dir):
        os.mkdir(end_dir)


    dfA = pd.DataFrame(pd.read_csv(dir_all, sep=";"))
    dfB = pd.DataFrame(pd.read_csv(dir_big, sep=";"))
    dfS = pd.DataFrame(pd.read_csv(dir_small, sep=";"))

    data_merged_right = pd.merge_ordered(dfB, dfS, how='outer')
    bs_column_names = ['SUBJECT BS', 'LABEL BS', 'DICE BS', 'HDRFDST BS']
    data_merged_right.columns = bs_column_names


    data_merged_right.to_csv(end_dir + 'Big_Small_Merged.csv', index=True)


    df_merged = pd.concat([dfA, data_merged_right], axis = 1)
    df_merged_smaller = df_merged.drop(axis=1, columns=['SUBJECT BS', 'LABEL BS'])

    df_merged_smaller.to_csv(end_dir + 'all_right.csv', index=True)


def main ():
    combine()

# for testing
if __name__ == '__main__':
    main()
