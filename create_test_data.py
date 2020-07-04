######################################################
#      Preprocessing code for 2020 Hackathon
#         Introduction to Machine Learning
#                   GitHub Task
#
#             Written By: Hadar Mulian
######################################################

import numpy as np
import pandas as pd


class ParseDiffFile:
    """
    given a diff file between two commits, this class will do the initial parsing of the file into
    coherent segments of code including initial filtration of non-informative non-unique or problematic chunks

    after filtration it is up to you to save or return the data chunks
    """

    def __init__(self, diff_path):
        self.added_lines_thr = 2
        self.minimal_words_thr = 10
        self.valid_line_lengths = np.arange(2, 6)
        self.valid_extensions = ['.py', '.js', '.go', '.h', '.cc', '.java', '.dart']
        self.segments = self.parse_diff_file(diff_path)

    def parse_diff_file(self, diff_path):
        initial_chunks = self.get_initial_chunks(diff_path)
        # print('initial chunks: ', initial_chunks[:5])
        return self.split2segments(initial_chunks)

    def worth_chunk(self, header):
        changes = header.split('@@')[1].split(' ')[1:-1]
        if ',' not in ''.join(changes):
            return False
        num_added = np.sum([int(x.split(',')[1]) if len(x.split(',')) > 1 else 0 for x in changes])
        return num_added >= self.added_lines_thr

    @staticmethod
    def get_extesions_diff_line(diff_line):
        fs = diff_line.replace('\n', '').split(' ')[-2:]
        exts = [x.split('.')[-1] for x in fs]
        return np.core.defchararray.add('.', exts)

    def is_relevant_diff(self, extensions):
        return np.sum(np.in1d(extensions, self.valid_extensions)) == len(extensions)

    def get_initial_chunks(self, diff_path):
        """
        does a first pass on the diff file and breaks it to chunks
        """
        chunks = np.empty(0)
        initial_lines = open(diff_path, "r").readlines()
        c = 17
        N = len(initial_lines)
        while c < N:
            line = initial_lines[c]
            if line.startswith('diff') and not self.is_relevant_diff(self.get_extesions_diff_line(line)):
                c += 1
                while c < N and not initial_lines[c].startswith('diff'):  # move to the next file
                    c += 1
                continue
            if line.startswith('@@') and self.worth_chunk(line):
                insert_c = 0
                curr_chunk = ''
                c += 1
                while c < N and not initial_lines[c].startswith('@@') and not initial_lines[c].startswith('diff'):
                    line = initial_lines[c]
                    if line.startswith('+'):  # added
                        insert_c += 1
                        curr_chunk += line[1:]
                    elif curr_chunk and insert_c >= self.added_lines_thr:  # deleted\not changed + non empty chunk
                        chunks = np.append(chunks, curr_chunk)
                        insert_c = 0
                    c += 1
                if curr_chunk and insert_c >= self.added_lines_thr:
                    chunks = np.append(chunks, curr_chunk)
            c += 1
        return chunks

    def create_segment(self, chunk_lines):
        seg_lens = np.random.choice(self.valid_line_lengths, len(chunk_lines))
        seg_ix = np.cumsum(seg_lens)
        seg_ix = seg_ix[seg_ix <= len(chunk_lines)]
        segs = np.array_split(chunk_lines, seg_ix)
        return ['\n'.join(s)+'\n' for s in segs if s.size > 1]  # filter faulty segments

    def split2segments(self, chunks):
        """takes each chunk of code and split it to code segments of 2-5 lines"""
        segments = []
        for i, chunk in enumerate(chunks):
            chunk_lines = chunk.split('\n')
            if len(''.join(chunk_lines).split(' ')) < self.minimal_words_thr:
                continue
            if len(chunk_lines) <= np.max(self.valid_line_lengths):
                segments += [chunk]
            else:
                segments += self.create_segment(chunk_lines)
        return segments

    def get_segments(self):
        return self.segments


def create_test_data():
    all_repos_path = '/cs/zbio/hadar/IML2020/tasks/github/data/july_3/'
    project_list = ['building_tools', 'espnet', 'horovod', 'jina', 'PaddleHub', 'PySolFC', 'pytorch_geometric']

    opt_segs = np.empty((0, 2))
    for repo_class, repo_name in enumerate(project_list):
        diff_path = '{}{}_diff.txt'.format(all_repos_path, repo_name)
        repo_segments = ParseDiffFile(diff_path).get_segments()
        repo_classes = np.full(len(repo_segments), repo_class)
        opt_segs_slice = np.column_stack((repo_classes, repo_segments))
        opt_segs = np.vstack((opt_segs, opt_segs_slice))
        print('number of segments from {} repo, is {}'.format(repo_name, len(repo_segments)))

    print('final amount of segments is {}'.format(opt_segs.shape[0]))
    test_seg_amount = 5000
    ix = np.random.choice(np.arange(opt_segs.shape[0]), test_seg_amount, replace=False)
    test_segs = opt_segs[ix, :]

    print('segd stats :',np.unique(test_segs[:,0].astype(int),return_counts=True))
    pd.DataFrame(test_segs).to_csv(all_repos_path+'test_data_full.tsv', sep='\t', header=False, index=False)


if __name__ == '__main__':
    create_test_data()
    # repo_segments = ParseDiffFile('PySolFC_diff.txt').get_segments()
    # repo_segments = ParseDiffFile('/cs/zbio/hadar/IML2020/tasks/github/data/july_3/PySolFC_diff.txt').get_segments()
    # print('##############################')
    # print('repo segments: ', repo_segments[:5])
