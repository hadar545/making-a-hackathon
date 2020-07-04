"""
===================================================
     Introduction to Machine Learning (67577)
             IML HACKATHON, June 2020

Author(s):

===================================================
"""
import numpy as np
from scipy.stats import entropy


class GitHubClassifier:

    def classify(self, X):
        """
        Receives a list of m unclassified pieces of code, and predicts for each
        one the Github project it belongs to.
        :param X: A numpy array of shape (m,) containing the code segments (strings)
        :return: y_hat - a numpy array of shape (m,) where each entry is a number between 0 and 6
        0 - building_tool
        1 - espnet
        2 - horovod
        3 - jina
        4 - PuddleHub
        5 - PySolFC
        6 - pytorch_geometric
        """
        m = X.shape[0]

        entr_vec = np.frombuffer(X[0].strip().encode(), dtype=np.uint8)
        seed = max(0, int(entropy(entr_vec)))
        np.random.seed(seed)

        return np.random.randint(0, 7, m)

if __name__ == '__main__':
    fc = GitHubClassifier()
    x = fc.classify(np.array(['sakdjf adskjf','sdf']))
    print(type(x))
