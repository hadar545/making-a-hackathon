import numpy as np
import argparse
import pandas as pd
import plotly.graph_objects as go


def visualize_task2_grade_weight():
    www_figs_dir = '/cs/usr/hadar545/www/figures/2020/july/'

    xx = np.linspace(0, 100, 100)
    yy = np.linspace(0, 1, 100)
    x, y = np.meshgrid(xx, yy)

    z = np.exp(-(x - 1) ** 2 - y ** 2) - 10 * (x ** 3 + y ** 4 - x / 5) * np.exp(-(x ** 2 + y ** 2))

    xyz_titles = np.array(['Theoretical Grade', 'Accuracy', 'Bonus Pts.'])
    fig = go.Figure(data=[go.Surface(z=z.T, x=x, y=y)])

    fig.update_layout(title='Grade Weighting for Github Classification', autosize=False, width=800, height=800,
                      margin=dict(l=65, r=50, b=65, t=90), scene=dict(xaxis_title=xyz_titles[0],
                                                                      yaxis_title=xyz_titles[1],
                                                                      zaxis_title=xyz_titles[2]))

    fig.write_html(www_figs_dir + 'IMl_Hack_github_weighting.html')


def assmeble_gr_comp_task2(theo_grade, acc):
    return 100, 7


def assmeble_gr_comp_task1(theo_grades, other_stats):
    return 100, 7


def get_finals(theo_grades_path, leaderboard_t1_path, leaderboard_t2_path):
    """
    creates csv file with three columns: CSE user, final_hack_grade, bonus_pts
    :param theo_grades: path to csv with the theoretical grades, first column is index of CSE users
    :param leaderboard_t1: path to csv with the format CSE_user, test_accuracy
    :param leaderboard_t2: path to csv with the format CSE_ser, test_accuracy, class (???) # TODO
    """
    theo_grades = pd.read_csv(theo_grades_path, header=None, index_col=0)
    leaderboard_t1 = pd.read_csv(leaderboard_t1_path, header=None, index_col=0)
    leaderboard_t2 = pd.read_csv(leaderboard_t2_path, header=None, index_col=0)

    all_users = theo_grades.index.values.flatten()
    task1_users = leaderboard_t1.index.values.flatten()
    task2_users = leaderboard_t2.index.values.flatten()

    final_stats = np.ones((theo_grades.shape[0], 2)) * (-1)
    for i, user in enumerate(all_users):
        if user in task1_users:
            final_stats[i, :] = assmeble_gr_comp_task1(theo_grades.iloc[i], leaderboard_t1.loc[user])
        elif user in task2_users:
            final_stats[i, :] = assmeble_gr_comp_task2(theo_grades.iloc[i], leaderboard_t1.loc[user].values.flatten())

    pd.DataFrame(final_stats, index=all_users).to_csv('final_stats.csv', header=False)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('theo_path', help='path to csv containing the theoretical grades')
    parser.add_argument('leaderboard1_path', help='path to csv containing the leaderboard of task1')
    parser.add_argument('leaderboard2_path', help='path to csv containing the leaderboard of task1')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    get_finals(args.theopath, args.leaderboard1_path, args.leaderboard2_path)
