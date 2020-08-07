import numpy as np
import argparse
import pandas as pd
import os, sys
from io import StringIO


def test_task1(test_data_dir):
    try:
        import warnings
        warnings.filterwarnings("ignore")
        sys.stdout = StringIO()
        path_to_weather_data = test_data_dir + '/all_weather_data.csv'
        test_features = pd.read_csv(test_data_dir + '/test_features.csv')
        test_labels = pd.read_csv(test_data_dir + '/test_labels.csv')

        sys.path.append(os.getcwd())
        import model
        fp = model.FlightPredictor(path_to_weather_data)
        prediction = fp.predict(test_features)

        loss1 = sum((prediction['PredArrDelay'] - test_labels['ArrDelay']) ** 2) / len(test_labels)
        gt_late = test_labels['ArrDelay'] > 0
        loss2gt = sum(prediction[gt_late]['PredDelayFactor'] == test_labels[gt_late]['DelayFactor'])
        loss2gt /= sum(gt_late)
        pred_late = prediction['PredArrDelay'] > 0
        loss2pred = sum(prediction[pred_late]['PredDelayFactor'] == test_labels[pred_late]['DelayFactor'])
        loss2pred /= sum(pred_late)

        sys.path.remove(os.getcwd())
        sys.stdout = sys.__stdout__
        return f'{loss1}, {loss2gt}, {loss2pred}'
    except Exception as e:
        sys.stdout = sys.__stdout__
        return e


def test_task2(test_data_dir):
    try:
        import warnings
        warnings.filterwarnings("ignore")
        sys.stdout = StringIO()
        sys.path.append(os.getcwd())
        import model
        # src_mod = __import__('{}.task2.src'.format(id_num), fromlist=['model'])

        test_segments = pd.read_csv(test_data_dir + '/test_data_full.tsv', sep='\t', header=None).values
        repo_class = test_segments[:, 0].astype(int).flatten()
        segments = test_segments[:, 1].astype(str).flatten()

        classifier = model.GitHubClassifier()
        repo_class_est = classifier.classify(segments)
        test_ma = repo_class == repo_class_est

        res = np.sum(test_ma) / repo_class.size

        sys.path.remove(os.getcwd())
        sys.stdout = sys.__stdout__
        return f'{res}'

    except Exception as e:
        sys.stdout = sys.__stdout__
        return e


def test_submission(task_type, id_num, test_data_dir):
    if task_type == 'task1':
        return test_task1(test_data_dir)
    elif task_type == 'task2':
        return test_task2(test_data_dir)
    else:
        print('Not a valid task type')
        return -1


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('task_type', help='type of task. options are: task1, task2')
    parser.add_argument('id_num', help='type of task. options are: task1, task2')
    parser.add_argument('test_data_dir', help='path ot a directory with test data')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    print(test_submission(args.task_type, args.id_num, args.test_data_dir))