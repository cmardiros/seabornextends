import scipy
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from datascienceutils import numpy_utils as np_utils
from datascienceutils import matplotlib_utils as mpl_utils


# TODO: move these

def sample_dist(samples,
                stat_func,
                title=None,
                fig_kws=None):

    # fig_kws = fig_kws or dict(size={'w': 4, 'h': 3}, dpi=150)
    fig_kws = fig_kws or dict(size={'w': 4.5, 'h': 3}, dpi=100)
    fig = plt.figure()

    if len(samples) > 1:
        colours = np.array(['steelblue', 'seagreen', 'red'])
    else:
        colours = np.array(['red'])

    for idx, (sample, kind) in enumerate(samples):
        ax = sns.distplot(sample)

    # NOTE: ensure vlines are plotted on top
    for idx, (sample, kind) in enumerate(samples):
        stat = stat_func(sample)
        ax.axvline(x=stat, color=colours[idx],
                   linestyle='solid',
                   label=' '.join([kind, stat_func.__name__]))
        sample_size = sample.shape[0]

    # finishing touches
    fig.set_size_inches(**fig_kws['size'])

    if title:
        t = '{0} distribution'.format(title)
        fig.suptitle(t=t, y=1.05)

    s = str()
    if len(samples) == 1:
        s = "stat={0:.3f}".format(stat)
        s += "~ sample_size={0}".format(sample_size)
        fig.text(x=0.5, y=-0.1, s=s,
                 verticalalignment='center',
                 horizontalalignment='center',
                 color='black')

    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    fig.set_dpi(fig_kws['dpi'])

    return fig


def qqplot(sample,
           distfit=stats.norm,
           title=None,
           fig_kws=None):

    # fig_kws = fig_kws or dict(size={'w': 4, 'h': 3}, dpi=150)
    fig_kws = fig_kws or dict(size={'w': 4.5, 'h': 3}, dpi=100)

    sample_size = sample.shape[0]

    # sort sample first
    sample = np.sort(sample, axis=0)

    fig = sm.ProbPlot(data=sample,
                      dist=distfit,
                      fit=True).qqplot(line='45',
                                       color='steelblue',
                                       markersize=5)

    # finishing touches
    fig.set_size_inches(**fig_kws['size'])

    if title:
        fig.suptitle(t=title, y=1.05)

    s = "sample_size={0}".format(sample_size)
    fig.text(x=0.5, y=-0.1, s=s,
             verticalalignment='center',
             horizontalalignment='center',
             color='black')
    fig.set_dpi(fig_kws['dpi'])

    return fig
