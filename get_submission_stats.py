#!/usr/bin/env python3

import numpy as np
import argparse
import pandas as pd
import os


def test_task1():
    return 0.5


def test_task2(id_num):
    src_mod = __import__('{}.task2.src'.format(id_num), fromlist=['model'])

    segs_path = '/cs/zbio/hadar/IML2020/tasks/github/data/july_3/test_data_full.tsv'
    test_segments = pd.read_csv(segs_path, sep='\t', header=None).values
    repo_class = test_segments[:, 0].astype(int).flatten()
    segments = test_segments[:, 1].astype(str).flatten()

    classifier = src_mod.model.GitHubClassifier()
    repo_class_est = classifier.classify(segments)
    test_ma = repo_class == repo_class_est

    return np.sum(test_ma) / repo_class.size


def test_submission(task_type, id_num):
    if task_type == 'task1':
        return test_task1()
    elif task_type == 'task2':
        return test_task2(id_num)
    else:
        print('Not a valid task type')
        return -1

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('task_type', help='type of task. options are: task1, task2')
    parser.add_argument('id_num', help='type of task. options are: task1, task2')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    print(test_submission(args.task_type, args.id_num))
