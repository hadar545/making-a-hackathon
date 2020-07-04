import numpy as np
import pandas as pd
from operator import itemgetter
import pandas as pd


def print_repr(file_path, line_num):
    """

    :param line_num: a number between 0 and file_length - 1
    :return: string representation of the line
    """
    with open(file_path) as fp:
        for i, line in enumerate(fp):
            if i == line_num:
                return line
            elif i > line_num:
                break


def get_project_classifications(values):
    repo_nums = {'building_tool': 0, 'espnet': 1, 'horovod': 2, 'jina': 3, 'PuddleHub': 4, 'PySolFC': 5,
                 'pytorch_geometric': 6}
    return itemgetter(*values)(repo_nums)


def create_example_data():
    repo_names = ['jina', 'horovod', 'pytorch_geometric']
    nums = [63, 203, 100]
    x = []
    for repo_name, num in zip(repo_names, nums):
        path = repo_name + '_all_data.txt'
        x += [print_repr(path, num)]
    print('input: {}'.format(np.array(x)))
    cls = get_project_classifications(repo_names)
    print('classification: {}'.format(np.array(cls)))

    # test saving
    pd.DataFrame(x).to_csv('demo_test_file.txt', index=False)
    d = pd.read_csv('demo_test_file.txt').values.flatten()


def create_repo_test_samples(full_test_path):
    file = open(full_test_path, 'r')
    datalines = np.array(file.readlines())
    file.close()

    lines_perc = [0.4, 0.2, 0.2, 0.1, 0.1]
    line_ops = np.arange(6)[1:]

    fences = np.random.choice(line_ops, size=datalines.size, p=lines_perc)
    slice_ix = np.cumsum(fences)
    max_valid_ix = np.max(np.where(slice_ix < datalines.size)[0])
    slice_ix = slice_ix[:max_valid_ix]

    # split the array
    splt_array = np.array_split(datalines, slice_ix)
    # merge each inner array to a single string
    test_set = [''.join(x) for x in splt_array]
    print(test_set)
    pd.DataFrame(test_set).to_csv('test_set.csv', index=False)

def mix_test_samples():
    # TODO: take test samples from the 7 repos and mix them in equal proportions to create a final test set
    pass
if __name__ == '__main__':
    # create_example_data()
    create_repo_test_samples('test_test.txt')
