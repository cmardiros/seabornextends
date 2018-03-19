import logging
import numpy as np
import seaborn as sns

from seabornextends.retouch.ax import AxRetoucher
from seabornextends.retouch.fig import FigRetoucher


class GridRetoucher(object):
    """
    Adds refinements to a Seaborn grid with one or more facets (Ax objects.
    """

    def add_tick_labels_vs_group_baseline(self,
                                          diffs,
                                          axis='xaxis',
                                          is_facetted=False,
                                          row=None,
                                          col=None):

        get_tick_locs_f = 'get_{0}ticks'.format(axis[0])
        get_tick_labels_f = 'get_{0}ticklabels'.format(axis[0])
        set_tick_locs_f = 'set_{0}ticks'.format(axis[0])
        set_tick_labels_f = 'set_{0}ticklabels'.format(axis[0])

        # print "diffs: {0}\n".format(diffs)

        for ax_retoucher in self.ax_retouchers:
            ax = ax_retoucher.ax

            tick_locs = getattr(ax, get_tick_locs_f)().tolist()
            # print "locs: {0}\n".format(tick_locs)

            existing_labels = [x.get_text() for x in
                               getattr(ax, get_tick_labels_f)()]
            # print "existing_labels: {0}\n".format(existing_labels)

            if not is_facetted:
                new_labels = list()
                for i, l in enumerate(existing_labels):

                    try:
                        extra_label = diffs[i][1]
                    except IndexError:
                        extra_label = ''

                    new_label = '\n'.join([l, extra_label])

                    new_labels.append(new_label)

            if is_facetted:
                facet_title = ax.get_title()

                # when grid is facetted only by col OR row
                if not all([row, col]):
                    facet, facet_level = facet_title.split('=')
                    facet_names = [str(facet_title.split('=')[0].strip())]
                    facet_levels = [str(facet_title.split('=')[1].strip())]
                else:
                    # when both row/col the title reflects levels for both
                    splitted = facet_title.split('|')
                    facet_names = [str(_.split('=')[0].strip())
                                   for _ in splitted]
                    facet_levels = [str(_.split('=')[1].strip())
                                    for _ in splitted]

                # if facet_level is int, try to convert it to int
                # (some categories are numerical but split produces strings)
                new = list()
                for fl in facet_levels:
                    try:
                        new.append(int(fl))
                    except Exception:
                        new.append(fl)
                        pass

                facet_levels = new
                # print "facet_names: {0}".format(facet_names)
                # print "facet_levels: {0}".format(facet_levels)

                # get relevant extra lebels to add just for this facet
                extras = list()
                for l in diffs:
                    if set(facet_levels).issubset(list(l[0])):
                        extras.append(l)
                # print "extras: {0}\n".format(extras)

                new_labels = list()
                for i, l in enumerate(existing_labels):

                    try:
                        extra_label = extras[i][1]
                    except IndexError:
                        extra_label = ''

                    new_label = '\n'.join([l, extra_label])

                    new_labels.append(new_label)

            # print "tick_locs: {0}".format(tick_locs)
            # print "new_labels: {0}\n".format(new_labels)
            getattr(ax, set_tick_locs_f)(tick_locs)
            getattr(ax, set_tick_labels_f)(new_labels)
