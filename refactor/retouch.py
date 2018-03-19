from datetime import datetime
import math
import pandas as pd
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from datascienceutils import pandas_utils
from datascienceutils import matplotlib_utils as mpl_utils


"""
Utils
"""





def tick_labels_vs_group_baseline(df,
                                  group_kws,
                                  estimator=np.mean,
                                  estimator_kws=None,
                                  decimals=1):

    df = pandas_utils.vs_group_baseline(df=df,
                                        group_kws=group_kws,
                                        estimator=estimator,
                                        estimator_kws=estimator_kws)

    base_key = group_kws['baseline_key']
    base_value = group_kws['baseline_value']

    df['vs'] = df['diff'] * 100
    df['vs'] = df['vs'].round(decimals)
    df['vs'] = df['vs'].apply(lambda x: str(x) + '%')

    # print "df_tick0:\n{0}\n".format(df.to_string())

    df.set_index(group_kws['groupby'], inplace=True)
    # df.loc[df[base_key] == base_value, 'vs'] = str()
    df.ix[df.index.get_level_values(base_key) == base_value, 'vs'] = str()

    # print "df_tick1:\n{0}\n".format(df.to_string())

    vs = [(index, row['vs']) for index, row in df.iterrows()]

    # print vs

    return vs


def _validate_seaborn_coords(coords):
    required_keys = sorted(['x', 'y', 'row', 'col', 'hue'])
    coords_keys = sorted(coords.keys())
    if required_keys != coords_keys:
        raise Exception("required_keys not match seaborn coords_keys")
    else:
        return coords


def get_coords_values(coords,
                      facets=False,
                      cats=False):
    """
    Given a dict of Seaborn coordinates return names of fields
    over which we will aggregate.

    Parameters:
    -----------
        facets: bool, optional
            If true only groupby keys for facetting will be returned
    """

    coords = _validate_seaborn_coords(coords)

    coords_with_values = {k: v for k, v in coords.iteritems() if v}

    # return groupby keys in the order closest to how data will
    # be aggregated in the plot
    groupby = list()

    possible_keys = list()
    if facets:
        possible_keys += ['col', 'row']
    if cats:
        possible_keys += ['x', 'y']

    if not facets and not cats:
        possible_keys = ['col', 'row', 'x', 'y', 'hue']

    for k in possible_keys:

        if coords_with_values.get(k):
            groupby.append(coords_with_values[k])

    return groupby


def factorplot_levels(df, coords):
    """
    Given a dictionary of Seaborn coordinates, return number
    of associated levels across all facets
    """
    coords = _validate_seaborn_coords(coords)

    keys = sorted([v for v in coords.values() if v])
    gb = df.groupby(keys)

    levels = pandas_utils.groups_as_dict(df, keys)
    n_levels = len(gb)

    return n_levels, levels


def factorplot_facets(df, coords):
    """
    Given a dictionary of Seaborn coordinates, return number
    of facets
    """
    coords = _validate_seaborn_coords(coords)

    keys = sorted([v for k, v in coords.iteritems()
                   if v and k in ['row', 'col']])
    gb = df.groupby(keys)

    levels = pandas_utils.groups_as_dict(df, keys)
    n_levels = len(gb)

    return n_levels, levels


def factorplot_axis_categories(df, coords):
    """
    Given a dictionary of Seaborn coordinates, return number
    of categories in each facet
    """
    coords = _validate_seaborn_coords(coords)

    keys = sorted([v for k, v in coords.iteritems()
                   if v and k in ['x', 'y']])
    gb = df.groupby(keys)

    levels = pandas_utils.groups_as_dict(df, keys)
    n_levels = len(gb)

    return n_levels, levels


def factorplot_facet_indices(df, coords):
    """
    Given a dictionary of Seaborn coords, return list of df indices
    in each facet in the order they will be plotted

    TODO: should hue be considered
    """

    coords = _validate_seaborn_coords(coords)

    keys = sorted([v for k, v in coords.iteritems()
                   if v and k in ['row', 'col']])
    gb = df.groupby(keys)

    return gb.indices


def factorplot_agg_indices(df, coords):
    """
    Given a dictionary of Seaborn coords, return list of original df
    indices which will be aggregated under each point.


    Use cases:
    ----------

    Determine whether plotting will result in df aggregation or not.
    """

    coords = _validate_seaborn_coords(coords)

    keys = sorted([v for k, v in coords.iteritems() if v])
    # print "keys: {0}\n".format(keys)
    gb = df.groupby(keys)
    # print "type(gb): {0}\n".format(type(gb))
    # print "gb.size(): {0}\n".format(gb.size())
    # print "dir(gb): {0}\n".format(dir(gb))

    is_agg = True

    levels = pandas_utils.groups_as_dict(df, keys)

    # gb.indices fails when there are too few rows to group
    try:
        indices = gb.indices
    except IndexError:
        indices = None

    if indices:
        # true if at least one point in factorplot will result in an
        # aggregation of several points
        is_agg = any([v.shape[0] > 1 for k, v in indices.iteritems()])

    return levels, indices, is_agg
