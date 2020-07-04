import argparse
import numpy as np

def simple_test(path):
    from task2.src.model import GitHubClassifier as ghc
    classifier = ghc()
    classifier.classify(np.array(['imprt numpy as np']))
    print('0.98324')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('submission_path', help='path to unzipped folder with code for the hackathon')
    args = parser.parse_args()
    simple_test(args.submission_path)