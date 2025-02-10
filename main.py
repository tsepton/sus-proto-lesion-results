import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math


def get_results():
    # https://usabilitygeek.com/how-to-use-the-system-usability-scale-sus-to-evaluate-the-usability-of-your-website/
    score = 0
    score_details = []
    results = {i: [0, 0, 0, 0, 0] for i in range(1, 11)}

    with open('results.csv', 'r') as csv_file:
        data = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        number_of_users = 0

        for _, row in enumerate(data):
            score_per_user = 0
            for index in range(1, 11):
                userAnswer = int(row[f'q{index}'])
                score_per_user += userAnswer - \
                    1 if (index % 2 == 1) else 5 - userAnswer
                results[index][userAnswer - 1] += 1

            score_per_user *= 2.5
            score_details.append(score_per_user)
            score += score_per_user
            number_of_users += 1
        score /= number_of_users

        for key in results:
            for index, value in enumerate(results[key]):
                results[key][index] = value / number_of_users * 100

    return results, score, score_details


def get_stacked_bar_chart(results, category_names, nb_participants):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    middle_index = data.shape[1]//2
    offsets = data[:, range(middle_index)].sum(
        axis=1) + data[:, middle_index]/2

    category_colors = plt.get_cmap('coolwarm_r')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths - offsets
        rects = ax.barh(labels, widths, left=starts, height=0.80,
                        label=colname, color=color)

        for rect, value in zip(rects, widths):
            width = rect.get_width()
            nb = math.ceil(round(value/100.0*nb_participants, 2))
            if (nb == 0):
                continue
            ax.text(width/2 + rect.get_x(), rect.get_y() + rect.get_height()/2,
                    f'{nb}', ha='center', va='center', color='black')

    ax.axvline(0, linestyle='--', color='black', alpha=.25)
    ax.set_xlim(-105, 105)
    ax.set_xticks(np.arange(-100, 101, 20))
    ax.xaxis.set_major_formatter(lambda x, pos: str(abs(int(x))))
    ax.invert_yaxis()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    fig.set_facecolor('#FFFFFF')

    return fig, ax


if (__name__ == "__main__"):

    # sus_category_names = [
    #     'Strongly disagree',
    #     'Disagree',
    #     'Neither agree nor disagree\t',
    #     'Agree',
    #     'Strongly agree'
    # ]

    sus_category_names = [
        'Pas du tout d\'accord',
        'Pas d\'accord',
        'Neutre',
        'D\'accord',
        'Tout à fait d\'accord'
    ]

    sus_results, sus_score, sus_per_user = get_results()
    sus_results = {f"Q{i+1}": sus_results[i+1] for i in range(0, 10)}

    print(f'Average SUS Score: {sus_score}')
    for userIndex, score in enumerate(sus_per_user):
        print(f'SUS Score for {userIndex}: {score}')

    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'text.usetex': True,
        'pgf.rcfonts': False,
    })
    text_width = 7.00697

    plt.rc('font', size=18)
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=18)
    plt.rc('legend', fontsize=18)

    fig, ax = get_stacked_bar_chart(
        sus_results, sus_category_names, len(sus_per_user))
    fig.legend(ncol=1, bbox_to_anchor=(0.5, -0.2),
               loc="lower center", borderaxespad=0)
    fig.set_size_inches(w=text_width, h=text_width*1.2)
    plt.savefig('output.pgf', dpi=1000, bbox_inches='tight')
    # plt.show()
