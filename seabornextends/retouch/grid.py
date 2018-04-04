import logging
import re
import numpy as np
import seaborn as sns

from seabornextends.retouch.ax import AxRetoucher
from seabornextends.retouch.fig import FigRetoucher
from seabornextends import utils


class FacetGridRetoucher(object):
    """
    Adds refinements to a Seaborn FacetGrid with
    one or more facets (Ax objects).
    """

    def __init__(self, grid, grid_kws=None):

        if not isinstance(grid, sns.FacetGrid):
            msg = "grid must be sns.FacetGrid but is {}".format(type(grid))
            logging.error(msg)
            raise ValueError(msg)

        self.grid = grid

        self._fig = self.grid.fig
        self.fig = FigRetoucher(self._fig)

        self.axes = [ax for ax in grid.axes.ravel()]
        self.ax_retouchers = [AxRetoucher(ax) for ax in self.axes]

        # a dict with grid params passed to seaborn
        # e.g. x, y, orient, row, col, hue, estimator, ci
        # TODO: should we make this a requirement?
        self.grid_kws = grid_kws or dict()

    def set_point_sizes(self,
                        sizes=None,
                        list_of_sizes=None):
        """
        If list of sizes, then one size list per ax
        """
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            if isinstance(list_of_sizes, (list, np.ndarray)):
                ax_retoucher.set_point_sizes(sizes=list_of_sizes[idx])
            elif sizes is not None:
                ax_retoucher.set_point_sizes(sizes=sizes)
            else:
                pass

    def set_point_colors(self,
                         colors=None,
                         list_of_colors=None):
        """
        If list of colors, then one size list per ax
        """
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            if isinstance(list_of_colors, (list, np.ndarray)):
                ax_retoucher.set_point_colors(colors=list_of_colors[idx])
            elif colors is not None:
                ax_retoucher.set_point_colors(colors=colors)
            else:
                pass

    def set_lines_colors(self,
                         colors=None,
                         list_of_colors=None):
        # TODO: len(colors) must match number of lines AND capsizes x2
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            if isinstance(list_of_colors, (list, np.ndarray)):
                ax_retoucher.set_lines_colors(colors=list_of_colors[idx])
            elif colors is not None:
                ax_retoucher.set_lines_colors(colors=colors)
            else:
                pass

    def set_lines_width(self,
                        width=1):
        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            ax_retoucher.set_lines_width(width=width)

    def set_lim(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_lim(**kwargs)

    def hide_axis_label(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.hide_axis_label(**kwargs)

    def set_visible(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_visible(**kwargs)

    def set_ticklabel_rotation(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_ticklabel_rotation(**kwargs)

    def touch_dates_axis(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.touch_dates_axis(**kwargs)

    def set_tick_params(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_tick_params(**kwargs)

    def set_label_size(self, **kwargs):
        for ax_retoucher in self.ax_retouchers:
            ax_retoucher.set_label_size(**kwargs)

    def add_legend(self, **kwargs):
        """
        Set using grid method but can't pass override loc
        """
        def_legend_kws = {
            'bbox_to_anchor': (1.05, 1),
            'borderaxespad': 0.0
        }
        kwargs = kwargs or dict()
        legend_kws = dict(def_legend_kws, **kwargs)
        self.grid.add_legend(**legend_kws)

    def set_annot(self, annot, **kwargs):
        """
        NOTE: set to first axis only
        """
        def_annot_kws = {
            'x': 0.5,
            'y': -0.3,
            'verticalalignment': 'top',
            'horizontalalignment': 'left',
            'color': 'black',
            'wrap': True
        }
        kwargs = dict(def_annot_kws, **kwargs)
        ax = self.ax_retouchers[0].ax
        ax.text(s=annot, transform=ax.transAxes, **kwargs)

    def highlight_lines(self,
                        values,
                        axis='yaxis',
                        styles_kws=None):

        styles_kws = styles_kws or list()

        if len(values) == 1:
            values = values * len(self.axes)

        if not styles_kws:
            styles_kws = [None] * len(self.axes)

        if len(styles_kws) == 1:
            styles_kws = styles_kws * len(self.axes)

        for idx, ax_retoucher in enumerate(self.ax_retouchers):
            ax_retoucher.highlight_line(axis=axis,
                                        value=values[idx],
                                        style_kws=styles_kws[idx])

    def highlight_levels(self,
                         df,
                         category,
                         highlights,
                         axis='xaxis'):
        """
        Draw h/v lines or bars to highlight one or more levels in a category.

        Example:

        # category is plotted on yaxis (y='country' in factorplot)
        retoucher.highlight_levels(
            df=df,
            category='country',
            axis='yaxis',
            highlights=[
                {'kind': 'bar', 'level_pattern': 'UK', 'color': 'C3'},
                {'kind': 'line', 'level_pattern': 'Australia', 'color': 'C4'},
                {'kind': 'capped_line', 'level_pattern': 'US', 'color': 'C9'}
            ])

        # category is plotted on xaxis (x='country' in factorplot)
        retoucher.highlight_levels(
            df=df,
            category='country',
            axis='xaxis',
            highlights=[
                {'kind': 'bar', 'level_pattern': 'UK', 'color': 'C3'},
                {'kind': 'line', 'level_pattern': 'Australia', 'color': 'C4'},
                {'kind': 'capped_line', 'level_pattern': 'US', 'color': 'C9'}
            ])

        bar / capped line: plot from 0 up to the aggregated value
        line: plots lines that extend to 100%
        """

        # what is the other axis
        other_axis = utils.other_axis(axis)
        logging.debug("other_axis: {}".format(other_axis))

        # what column in the df is plotted on this other axis
        other_axis_column = self.grid_kws[other_axis]

        # the estimator used to summarize the df
        estimator = self.grid_kws['estimator']

        for highlight in highlights:

            # what kind of highlight will be plotted
            valid_kinds = ['line', 'bar', 'capped_line']
            kind = highlight.get('kind') or 'line'
            if kind not in valid_kinds:
                raise Exception("kind must be one of {} but is {}".format(
                    kind,
                    valid_kinds))

            level_pattern = highlight['level_pattern']
            color = highlight.get('color') or 'r'
            alpha = highlight.get('alpha') or 1
            style = highlight.get('style') or 'solid'
            width = highlight.get('width') or 1.5

            # mapping of the functions we will use to highlight
            mapping = {
                'line': {
                    'xaxis': 'axvline',
                    'yaxis': 'axhline'
                },
                'capped_line': {
                    'xaxis': 'vlines',
                    'yaxis': 'hlines'
                },
                'bar': {
                    'xaxis': 'bar',
                    'yaxis': 'barh'
                }
            }

            highlighter = mapping[kind][axis]

            # get all levels for the plotted category
            try:
                levels = df[category].cat.categories.tolist()
            except AttributeError:
                msg = "'{}' must be a category".format(category)
                logging.error(msg)
                raise AttributeError(msg)
            except Exception:
                raise

            # see which levels match the ones we want to highlight
            # and get their index
            logging.debug("level_pattern: {}".format(level_pattern))
            pattern = re.compile(str(level_pattern))
            matches = [str(l) for l in levels if pattern.search(str(l))]
            matches_idx = [i for i, l in enumerate(levels)
                           if pattern.search(str(l))]

            logging.debug("matches: {}".format(matches))
            logging.debug("matches_idx: {}".format(matches_idx))

            for idx, ax_retoucher in enumerate(self.ax_retouchers):
                ax = ax_retoucher.ax
                for level_idx in matches_idx:

                    # get all values for the level we wish to highlight
                    filtered = df[df[category].astype('str').isin(matches)]
                    values = filtered[other_axis_column]
                    estimate = estimator(values)

                    if kind == 'line':
                        getattr(ax, highlighter)(
                            level_idx,
                            linestyle=style,
                            linewidth=width,
                            color=color,
                            alpha=alpha)

                    if kind == 'capped_line':
                        getattr(ax, highlighter)(
                            level_idx,
                            0,
                            estimate,
                            linestyle=style,
                            linewidth=width,
                            color=color,
                            alpha=alpha)

                    elif kind == 'bar':
                        getattr(ax, highlighter)(
                            level_idx,
                            estimate,
                            color=color,
                            alpha=alpha)


class JointGridRetoucher(object):
    """
    Adds refinements to a Seaborn JointGrid with
    one or more facets (Ax objects).
    """

    def __init__(self, grid, grid_kws=None):

        if not isinstance(grid, sns.JointGrid):
            msg = "grid must be sns.JointGrid but is {}".format(type(grid))
            logging.error(msg)
            raise ValueError(msg)

        self.grid = grid

        self._fig = self.grid.fig
        self.fig = FigRetoucher(self._fig)

        self.axes = {'joint': grid.ax_joint,
                     'marg_x': grid.ax_marg_x,
                     'marg_y': grid.ax_marg_y}

        self.ax_retouchers = {n: AxRetoucher(ax) for n, ax in self.axes.items()}

        # a dict with grid params passed to seaborn
        # e.g. x, y, orient, row, col, hue, estimator, ci
        # TODO: should we make this a requirement?
        self.grid_kws = grid_kws or dict()
