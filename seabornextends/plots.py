import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot(x,
         y,
         plot_kws=None,
         **facetgrid_kws):
    """
    Facetted version of plt.plot.

    Example:
    plot(x='ad_spend',
         y='conversions',
         data=df,
         row='loc',
         col='scale',
         plot_kws={'lineweight': 3})

    """

    plot_kws = plot_kws or dict()

    grid = sns.FacetGrid(**facetgrid_kws)

    grid.map(plt.plot, x, y, **plot_kws)

    return grid


def distplot(a,
             distplot_kws=None,
             **facetgrid_kws):
    """
    Facetted version of seaborn distplot.

    Example:
    distplot(a='order_value',
             data=df,
             row='loc',
             col='scale',
             distplot_kws={'hist': False, 'kde': True})
    """

    distplot_kws = distplot_kws or dict()

    if isinstance(a, pd.Series):
        raise Exception("a must be name of series in df not pd.Series")

    grid = sns.FacetGrid(**facetgrid_kws)

    grid.map(sns.distplot, a, **distplot_kws)
    return grid


def violinplot(a,
               violin_kws=None,
               **facetgrid_kws):
    """
    Facetted version of seaborn violinplot.

    Example:
    violinplot(a='order_value',
               data=df,
               row='loc',
               col='scale',
               box_kws={'orient': 'v'})
    """

    violin_kws = violin_kws or dict()

    if isinstance(a, pd.Series):
        raise Exception("a must be name of series in df not pd.Series")

    grid = sns.FacetGrid(**facetgrid_kws)

    grid.map(sns.violinplot, a, **violin_kws)

    return grid


def boxplot(a,
            box_kws=None,
            **facetgrid_kws):
    """
    Facetted version of seaborn boxplot.

    Example:
    boxplot(a='order_value',
            data=df,
            row='loc',
            col='scale',
            box_kws={'orient': 'v'})
    """

    box_kws = box_kws or dict()

    if isinstance(a, pd.Series):
        raise Exception("a must be name of series in df not pd.Series")

    grid = sns.FacetGrid(**facetgrid_kws)

    grid.map(sns.boxplot, a, **box_kws)

    return grid
