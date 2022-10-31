"""seperation of labels

Seperates the small and the bigger structure from the test files and puts it to new folder
"""
import os
import sys
import shutil



src_file = os.path.join((os.path.dirname(sys.argv[0])), '../data/test/')
shutil.copy2(src_file,src_file)




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